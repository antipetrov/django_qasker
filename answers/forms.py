# coding: utf-8
__author__ = 'petrmatuhov'

from django.forms import ModelForm

from django.forms.widgets import Widget, Input, Textarea
from django.forms.utils import ErrorList
from django.contrib.auth.forms import UserCreationForm

from models import Question

class AskForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(AskForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Question
        fields = ['title', 'content', 'tags']
        labels = {'title': 'Title', 'content': 'Question', 'tags':'Tags'}

        widgets = {
            'title': Input(attrs={'class': 'form-control'}),
            'content': Textarea(attrs={'class': 'form-control'}),
            'tags': Input(attrs={'class': 'form-control'}),
        }


class SignupForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)



