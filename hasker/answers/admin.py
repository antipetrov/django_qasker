# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Question, Answer, Tag, User

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register(User, UserAdmin)