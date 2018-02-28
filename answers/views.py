# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from forms import AskForm, SignupForm
from models import Question, Tag, Answer


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
        username = request.POST.get('username')
        password = request.POST.get('password')
        
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


def user_signup(request):
    return render(request, 'answers/signup.html', {})


@login_required
def ask_question(request):
    if request.method == 'POST':
        new_question = Question(author=request.user, create_date=datetime.datetime.now())

        form = AskForm(request.POST, instance=new_question)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            pass
    else:
        form = AskForm()

    return render(request, 'answers/ask.html', {'form': form})


@login_required
def list_tags_json(request):

    tags = {tag.id: tag.name for tag in Tag.objects.all()}
    return HttpResponse(json.dumps(tags))


@login_required
def view_question(request, question_id):
    errors = []
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")

    if request.method == 'POST':

        # validate
        answer_text = request.POST.get('answer')
        if not answer_text:
            errors.append('Empty answer not allowed')

        answer_text = answer_text[:8192]

        try:
            new_answer = Answer()
            new_answer.question = question
            new_answer.author = request.user
            new_answer.content = answer_text
            new_answer.create_date = datetime.datetime.now()

            new_answer.save()
        except Exception as e:
            errors.append("Unable to save answer: %s" % e.message)

        if not errors:
            redirect('view_question', question.id)

    return render(request, 'answers/answer.html', {'question': question, 'errors':errors})


@login_required
def view_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404("Question does not exist")

    return render(request, 'answers/user.html', {'user': user})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return render(request, 'answers/signup_complete.html')
    else:
        form = SignupForm()

    return render(request, 'answers/signup.html', {'form': form})


def search_result(request):
    return HttpResponse("Search result Page")
