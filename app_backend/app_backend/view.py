from django.http import HttpResponse
from django.shortcuts import render


def hello(request):
    return HttpResponse("Hello world ! ")


def render_hello(request):
    context = {'hello': 'Hello World!'}
    return render(request, 'test_hello.html', context)
