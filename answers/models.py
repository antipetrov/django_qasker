# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(primary_key=True, max_length=255)

    def __str__(self):
        return "[%s]" % self.name


class Question(models.Model):
    author = models.ForeignKey(User, null=False,)
    create_date = models.DateTimeField('date created', db_index=True, null=False)
    title = models.CharField(max_length=255, null=False)
    content = models.TextField()
    rating = models.IntegerField(default=0, null=False, db_index=True)
    tags = models.ManyToManyField(Tag)
    votes = models.ManyToManyField(User, related_name='voted_questions')

    def __str__(self):
        return "%s:%s"%(self.title, self.content[:200])


class Answer(models.Model):
    author = models.ForeignKey(User, null=False)
    create_date = models.DateTimeField('date created', db_index=True, null=False)
    question = models.ForeignKey(Question, null=False, related_name='answers')
    content = models.TextField()
    rating = models.IntegerField(default=0, null=False, db_index=True)
    votes = models.ManyToManyField(User, related_name='voted_answers')
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return "%s:%s"%(self.question.title, self.content[:200])


class UserProfile(models.Model):
    user = models.ForeignKey(User, related_name='profile')
    avatar_href = models.FileField(upload_to='uploads/', null=True)