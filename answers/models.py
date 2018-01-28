# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    author = models.ForeignKey(User)
    create_date = models.DateTimeField('date created', db_index=True)
    title = models.CharField(max_length=255)
    content = models.TextField()

class Answer(models.Model):
    user = models.ForeignKey(User)
    create_date = models.DateTimeField('date created', db_index=True)
    question = models.ForeignKey(Question)
    content = models.TextField()

class Tag(models.Model):
    name = models.CharField(max_length=255, db_index=True)
