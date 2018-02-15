# coding: utf-8
__author__ = 'petrmatuhov'

from django import forms
from django.forms.utils import ErrorList
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from models import Question, UserProfile

class AskForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AskForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Question
        fields = ['title', 'content', 'tags']
        labels = {'title': 'Title', 'content': 'Question', 'tags':'Tags'}

        widgets = {
            'title': forms.widgets.Input(attrs={'class': 'form-control'}),
            'content': forms.widgets.Textarea(attrs={'class': 'form-control'}),
            'tags': forms.widgets.Input(attrs={'class': 'form-control'}),
        }


class SignupForm(UserCreationForm):

    email = forms.EmailField(required=True)
    avatar = forms.FileField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "avatar")
        widgets = {
            'username': forms.widgets.Input(attrs={'class': 'form-control'}),
            'email': forms.widgets.Input(attrs={'class': 'form-control'}),
            'password1': forms.widgets.Input(attrs={'class': 'form-control'}),
            'password2': forms.widgets.Input(attrs={'class': 'form-control'}),
            'avatar': forms.widgets.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        new_user = super(SignupForm, self).save(*args, **kwargs)

        if new_user:
            new_profile = UserProfile()
            new_profile.user = new_user
            new_profile.avatar_href = self.cleaned_data.get('avatar')



