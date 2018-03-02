# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import json

from django.db import transaction
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseNotAllowed
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from forms import AskForm, SignupForm
from models import Question, Tag, Answer
from django import urls


def _parse_search(search_term):
    tags = []
    words = []
    formatted_term = ''

    if search_term:
        parts = [p.strip() for p in search_term.split(' ')]
        for part in parts:
            if part.startswith('tag:'):
                tags.append(part[4:])
            else:
                words.append(part)

        formatted_term = " ".join(["tag:%s"%tag for tag in tags]) + " " + " ".join(words)

    search_dict = {
            "words": words,
            "tags": tags,
            "full_term": formatted_term
        }

    return search_dict


def _paginate(objects, page, on_page=5):

    paginator = Paginator(objects, on_page)

    try:
        objects_page = paginator.page(page)
    except PageNotAnInteger:
        objects_page = paginator.page(1)
    except EmptyPage:
        objects_page = paginator.page(paginator.num_pages)

    return objects_page


def index(request):
    page = request.GET.get('page')
    question_page = _paginate(Question.objects.presorted(), page)

    topquestions = Question.objects.presorted()[:10]


    return render(request, 'answers/index.html', {"questions": question_page,
                                                  "topquestions": topquestions
                                                  })


def search_result(request):
    search_dict = _parse_search(request.GET.get('q'))

    questions = Question.objects
    if not search_dict['words'] and not search_dict['tags']:
        questions = questions.presorted()
    else:
        if search_dict['tags']:
            questions = questions.filter(tags__name__in=search_dict['tags'])

        if search_dict['words']:
            search_term = ' '.join(search_dict['words'])
            questions = questions.filter(Q(title__contains=search_term) | Q(content__contains=search_term))

    topquestions = Question.objects.presorted()

    page = request.GET.get('page')
    questions = _paginate(questions, page)

    return render(request, 'answers/index.html', {
        "questions": questions,
        "topquestions": topquestions,
        "search": search_dict
        })


def tag_result(request, tag):
    search_dict = _parse_search("tag:%s" % tag)
    questions = Question.objects.presorted().filter(tags__name__in=search_dict['tags'])

    topquestions = Question.objects.presorted()

    page = request.GET.get('page')
    questions = _paginate(questions, page)

    return render(request, 'answers/index.html', {"questions": questions,
                                                  "topquestions": topquestions,
                                                  "search": search_dict})


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

    term = request.GET.get('term')

    if term:
        tags = list(tag.name for tag in Tag.objects.filter(name__startswith=term)[:20])
    return HttpResponse(json.dumps(tags))


@login_required
def view_question(request, question_id):
    errors = []
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")

    is_my = (request.user.id == question.author.id)

    if request.method == 'POST':

        # validate
        answer_text = request.POST.get('answer')
        if not answer_text:
            errors.append('Empty answer not allowed')

        answer_text = answer_text[:8192]

        with transaction.atomic():
            try:
                new_answer = Answer()
                new_answer.question = question
                new_answer.author = request.user
                new_answer.content = answer_text
                new_answer.create_date = datetime.datetime.now()

                new_answer.save()
            except Exception as e:
                errors.append("Unable to save answer: %s" % e.message)

            question.answers_count = Answer.objects.filter(question_id=question.id).count()
            question.save()

        if not errors:
            redirect('view_question', question.id)


    return render(request, 'answers/answer.html', {'question': question,
                                                   'errors': errors,
                                                   'is_my': is_my})


@login_required
def question_vote(request, question_id, action):
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")

    with transaction.atomic():
        if action == 'plus':
            question.votes.add(request.user)
        else:
            question.votes.remove(request.user)

        # update rating
        question.rating = question.votes.count()
        question.save()

    return redirect('view_question', question.id)


@login_required
def answer_vote(request, question_id, answer_id, action):
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")

    try:
        answer = Answer.objects.prefetch_related('votes').get(id=answer_id)
    except Question.DoesNotExist:
        raise Http404("Answer does not exist")

    if answer.question_id != question.id:
        raise Http404("Answer not found")

    with transaction.atomic():
        if action == 'plus':
            answer.votes.add(request.user)
        else:
            answer.votes.remove(request.user)

        # update rating
        answer.rating = answer.votes.count()
        answer.save()

        return redirect('view_question', question.id)


@login_required
def answer_accept(request, answer_id):
    try:
        answer = Answer.objects.get(id=answer_id)
    except Question.DoesNotExist:
        raise Http404("Answer does not exist")

    if not answer.author == request.user:
        raise HttpResponseNotAllowed("You cannot mark someone elses answer")

    with transaction.atomic():
        if not answer.is_accepted:
            # if going to accept
            Answer.objects.filter(question=answer.question).update(is_accepted=False)

        answer.is_accepted = not answer.is_accepted
        answer.save()

    return redirect('view_question', answer.question_id)


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
