# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from models import Question

# Create your views here.
def index(request):
    questions = Question.objects.all()

    return render(request, 'answers/index.html', {"questions": questions})

def user_login(request):
    context = {}

    if request.method == 'POST':
        errors = []
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        if not username:
            errors.append('no username')

        if not username:
            errors.append('no password')

        if errors:
            context = { 'errors': errors }
            return render(request, 'answers/login.html', context)

        user = authenticate(request, username=username, password=password)        
        if user:
            login(request, user)
            return redirect('index')
        else:
            context = {'errors': ['Invalid login or password']}
    
    return render(request, 'answers/login.html', context)

def user_logout(request):
    logout(request)
    return redirect('index')


def ask_question(request):
    return HttpResponse("Ask Question Page")

def view_question(request, code):
    return HttpResponse("View Question Page %s" % code)

def search_result(request):
    return HttpResponse("Search result Page")
