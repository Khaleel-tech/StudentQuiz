from django.urls import path

from .views import (
    ChatbotPageView,
    HomeView,
    LeaderboardView,
    QuizHistoryView,
    QuizView,
    chatbot_api,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('quiz/', QuizView.as_view(), name='quiz'),
    path('history/', QuizHistoryView.as_view(), name='history'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    path('chatbot/', ChatbotPageView.as_view(), name='chatbot'),
    path('api/chatbot/', chatbot_api, name='chatbot_api'),
]
