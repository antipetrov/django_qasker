# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    context = {'ctn': 1}
    return render(request, 'answers/index.html', context)

def ask_question(request):
    return HttpResponse("Ask Question Page")

def view_question(request, code):
    return HttpResponse("View Question Page %s" % code)

def search_result(request):
    return HttpResponseResponse("Search result Page")
