from django.shortcuts import render
from django.http import HttpResponse
from .models import Question
# Create your views here.

def detail(request, question_id):
    return HttpResponse("youre looking at question %s." % question_id)

def results(request, question_id):
    response = "youre looking at the results of question %s."
    return HttpResponse(response % question_id)

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    context = { 
         'latest_question_list': latest_question_list,
    } 
    return HttpResponse("Hello, world!")
