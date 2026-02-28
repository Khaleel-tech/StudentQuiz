from django.contrib import admin

from .models import Question, Score


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'difficulty', 'correct_answer')
    list_filter = ('difficulty',)
    search_fields = ('question_text',)


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'total', 'percentage', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username',)
    readonly_fields = ('created_at',)
