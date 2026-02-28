import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, ListView, TemplateView

from .forms import QuizFilterForm, UserRegisterForm
from .models import Question, Score


class HomeView(TemplateView):
    template_name = 'quiz_app/home.html'


class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')


class QuizView(LoginRequiredMixin, View):
    template_name = 'quiz_app/quiz.html'
    result_template_name = 'quiz_app/result.html'

    def get(self, request):
        filter_form = QuizFilterForm(request.GET or None)
        questions = Question.objects.all()
        selected_difficulty = ''
        if filter_form.is_valid():
            selected_difficulty = filter_form.cleaned_data.get('difficulty') or ''
            if selected_difficulty:
                questions = questions.filter(difficulty=selected_difficulty)

        context = {
            'questions': questions,
            'filter_form': filter_form,
            'selected_difficulty': selected_difficulty,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        difficulty = request.POST.get('difficulty', '')
        questions = Question.objects.filter(difficulty=difficulty) if difficulty else Question.objects.all()
        total = questions.count()
        correct_count = 0
        question_results = []

        for question in questions:
            selected = request.POST.get(f'question_{question.id}', '')
            is_correct = selected == question.correct_answer
            if is_correct:
                correct_count += 1
            question_results.append(
                {
                    'question': question,
                    'selected': selected,
                    'is_correct': is_correct,
                }
            )

        percentage = (correct_count / total * 100) if total else 0.0
        performance_message = self._build_performance_message(percentage)

        Score.objects.create(
            user=request.user,
            score=correct_count,
            total=total,
            percentage=round(percentage, 2),
        )

        context = {
            'score': correct_count,
            'total': total,
            'percentage': round(percentage, 2),
            'performance_message': performance_message,
            'question_results': question_results,
        }
        return render(request, self.result_template_name, context)

    @staticmethod
    def _build_performance_message(percentage: float) -> str:
        if percentage >= 85:
            return 'Outstanding work! You have mastered this topic.'
        if percentage >= 65:
            return 'Great job! Keep practicing to score even higher.'
        if percentage >= 40:
            return 'Good effort! Review explanations and try again.'
        return 'Keep learning! Revisit the basics and take another quiz.'


class QuizHistoryView(LoginRequiredMixin, ListView):
    template_name = 'quiz_app/history.html'
    context_object_name = 'scores'

    def get_queryset(self):
        return Score.objects.filter(user=self.request.user)


class LeaderboardView(ListView):
    template_name = 'quiz_app/leaderboard.html'
    context_object_name = 'leaders'

    def get_queryset(self):
        return (
            User.objects.filter(scores__isnull=False)
            .annotate(best_percentage=Max('scores__percentage'))
            .order_by('-best_percentage', 'username')[:10]
        )


class ChatbotPageView(TemplateView):
    template_name = 'quiz_app/chatbot.html'


@require_POST
def chatbot_api(request):
    try:
        payload = json.loads(request.body)
        message = (payload.get('message') or '').strip().lower()
    except json.JSONDecodeError:
        return JsonResponse({'response': 'Invalid JSON payload.'}, status=400)

    knowledge_base = {
        'python': 'Python is a versatile language used for web, data science, automation, and AI.',
        'oop': 'OOP stands for Object-Oriented Programming: encapsulation, inheritance, polymorphism, and abstraction.',
        'machine learning': 'Machine learning enables systems to learn from data and improve predictions without explicit programming.',
        'data science': 'Data science combines statistics, programming, and domain expertise to extract insights from data.',
        'interview preparation': 'Interview prep tip: practice DSA, review projects, and rehearse concise STAR-format answers.',
    }

    for topic, answer in knowledge_base.items():
        if topic in message:
            return JsonResponse({'response': answer})

    fallback = (
        'I can help with python, oop, machine learning, data science, and interview preparation. '
        'Please ask about one of these topics.'
    )
    return JsonResponse({'response': fallback})
