# coding: utf-8
__author__ = 'petrmatuhov'

from datetime import datetime

from django import forms
from django.forms.utils import ErrorList
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.core.exceptions import ValidationError

from django.utils.translation import ugettext, ugettext_lazy as _

from models import Question, User, Tag
from widgets import TagsInput, ImageInput


class TagsField(forms.Field):
    def __init__(self, max_length, *args, **kwargs):
        super(TagsField, self).__init__(*args, **kwargs)
        self.max_length = max_length

    def to_python(self, value):
        if not value:
            return []

        return value.split(',')

    def validate(self, value):
        super(TagsField, self).validate(value)
        if len(value) > self.max_length:
            raise ValidationError("Too much tags. %s is maximum" % self.max_length, code='max_length')

    def value_from_object(self, obj):
        """
        Return all related tagnames
        """
        return ','.join([row.name for row in self.related_model.objects.all()])


class AskForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content', 'tags']

    title = forms.CharField(max_length=64, label='Title', strip=True, required=True,
                            widget=forms.widgets.Input(attrs={'class': 'form-control'}))
    content = forms.CharField(max_length=255, label='Text', strip=True, required=True,
                              widget=forms.widgets.Textarea(attrs={'class': 'form-control'}))
    tags = TagsField(max_length=3, widget=TagsInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(AskForm, self).__init__(*args, **kwargs)


    def _save_m2m(self):
        # add new tags
        tags = self.cleaned_data['tags']
        tags_qs = Tag.objects.filter(name__in=tags).all()

        new_tags = set(tags) - set(row.name for row in tags_qs)
        for t in new_tags:
            new_tag = Tag()
            new_tag.name = t
            new_tag.save()

        super(AskForm, self)._save_m2m()



class SignupForm(forms.ModelForm):

    username = forms.CharField(max_length=64, strip=True,
                               widget=forms.widgets.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(max_length=64, strip=True,
                                widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(max_length=64, strip=True,
                                widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.widgets.EmailInput(attrs={'class': 'form-control'}))
    avatar = forms.FileField(widget=ImageInput(attrs={'class': 'form-control'}), required=False)

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

        password_validation.validate_password(password2)

        return password2

    @transaction.atomic
    def save(self, *args, **kwargs):
        # user = User()
        # user.username = self.cleaned_data['username']
        # user.set_password(self.cleaned_data["password1"])
        # user.email = self.cleaned_data['email']
        # user.date_joined = datetime.now()
        # user.save()

        new_user = super(SignupForm, self).save(*args, **kwargs)
        new_user.set_password(self.cleaned_data["password1"])
        # new_user.avatar = self.cleaned_data.get('avatar')
        new_user.save()

        # new_profile = User()
        # new_profile.user = new_user
        # new_profile.avatar_href = self.cleaned_data.get('avatar')
        # new_profile.save()

        return new_user



