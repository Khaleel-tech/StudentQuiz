from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Question


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class QuizFilterForm(forms.Form):
    difficulty = forms.ChoiceField(
        required=False,
        choices=[('', 'All Difficulties')] + list(Question.Difficulty.choices),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
