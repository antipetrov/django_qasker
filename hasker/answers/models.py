# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser

from django.utils.timezone import get_current_timezone, make_aware, utc, now


class User(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/', null=True)


class Tag(models.Model):
    name = models.CharField(primary_key=True, max_length=255)

    def __str__(self):
        return "[%s]" % self.name


class QuestionManager(models.Manager):
    def top_rating(self, **kwargs):
        return self.prefetch_related('tags').select_related('author').\
            order_by('-rating', '-create_date')


class Question(models.Model):
    author = models.ForeignKey(User, null=False,)
    create_date = models.DateTimeField('date created', db_index=True,
                                       null=False)
    title = models.CharField(max_length=255, null=False)
    content = models.TextField()
    rating = models.IntegerField(default=0, null=False, db_index=True)
    answers_count = models.IntegerField(default=0, null=False, db_index=True)
    tags = models.ManyToManyField(Tag)
    votes = models.ManyToManyField(User, related_name='voted_questions')

    def time_from_now(self):
        return now() - self.create_date

    def __str__(self):
        return "%s:%s"%(self.title, self.content[:200])

    objects = QuestionManager()


class AnswerManager(models.Manager):
    def top_rating(self, **kwargs):
        return self.select_related('author').order_by('-is_accepted',
                                                      '-rating', '-create_date')


class Answer(models.Model):
    author = models.ForeignKey(User, null=False)
    create_date = models.DateTimeField('date created', db_index=True,
                                       null=False)
    question = models.ForeignKey(Question, null=False, related_name='answers')
    content = models.TextField()
    rating = models.IntegerField(default=0, null=False, db_index=True)
    votes = models.ManyToManyField(User, related_name='voted_answers')
    is_accepted = models.BooleanField(default=False)

    def time_from_now(self):
        return now() - self.create_date

    objects = AnswerManager()

    def __str__(self):
        return "%s:%s" % (self.question.title, self.content[:200])




# class UserProfile(models.Model):
#     user = models.ForeignKey(User, related_name='profile')
#     avatar_href = models.FileField(upload_to='uploads/', null=True)
#
#
