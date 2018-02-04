# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    author = models.ForeignKey(User)
    create_date = models.DateTimeField('date created', db_index=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.IntegerField(default=0, null=False, db_index=True)

    def __str__(self):
            return "%s:%s"%(self.title, self.content[:200])


class Answer(models.Model):
    user = models.ForeignKey(User)
    create_date = models.DateTimeField('date created', db_index=True)
    question = models.ForeignKey(Question)
    content = models.TextField()
    rating = models.IntegerField(default=0, null=False, db_index=True)

    def __str__(self):
        return "%s:%s"%(self.question.title, self.content[:200])


class Tag(models.Model):
    name = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.name
