# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm

from models import Question


# Create your views here.
def index(request):
    # todo: sort by rating
    questions = Question.objects.all()
    topquestions = Question.objects.all()

    return render(request, 'answers/index.html', {"questions": questions,
                                                  "topquestions": topquestions})

def user_login(request):
    ctx = {}
    if request.method == 'POST':
        errors = []
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        if not username:
            errors.append('no username')

        if not username:
            errors.append('no password')

        if errors:
            ctx = { 'errors': errors }
            return render(request, 'answers/login.html', ctx)

        user = authenticate(request, username=username, password=password)        
        if user:
            login(request, user)
            return redirect('index')
        else:
            ctx = {'errors': ['Invalid login or password']}
    
    return render(request, 'answers/login.html', ctx)


def user_logout(request):
    logout(request)
    return redirect('index')


class AskForm(ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content']
        labels = {'title': 'TItle', 'content': 'Question'}

@login_required
def ask_question(request):
    if request.method == 'POST':
        form = AskForm(request.POST)
    else:
        form = AskForm()

    return render(request, 'answers/ask.html', {'form': form})

def view_question(request, code):
    return HttpResponse("View Question Page %s" % code)

def search_result(request):
    return HttpResponse("Search result Page")
