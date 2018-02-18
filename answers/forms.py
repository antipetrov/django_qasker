# coding: utf-8
__author__ = 'petrmatuhov'

from datetime import datetime

from django import forms
from django.forms.utils import ErrorList
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.utils.translation import ugettext, ugettext_lazy as _

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


class SignupForm(forms.ModelForm):

    username = forms.CharField(max_length=64, strip=True, widget=forms.widgets.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(max_length=64, strip=True, widget=forms.widgets.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(max_length=64, strip=True, widget=forms.widgets.PasswordInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.widgets.EmailInput(attrs={'class': 'form-control'}))
    avatar = forms.FileField(widget=forms.widgets.FileInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'avatar')

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    @transaction.atomic
    def save(self, *args, **kwargs):
        # user = User()
        # user.username = self.cleaned_data['username']
        # user.set_password(self.cleaned_data["password1"])
        # user.email = self.cleaned_data['email']
        # user.date_joined = datetime.now()
        # user.save()

        user = super(SignupForm, self).save(*args, **kwargs)
        user.set_password(self.cleaned_data["password1"])
        user.save()

        new_profile = UserProfile()
        new_profile.user = user
        new_profile.avatar_href = self.cleaned_data.get('avatar')
        new_profile.save()



