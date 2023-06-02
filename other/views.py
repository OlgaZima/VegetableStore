from django.shortcuts import render

# Create your views here.
from datetime import datetime
from django.views import View
from django.http import HttpResponse
from random import random
from django.shortcuts import render

class currentDateView(View):

    def get(self, request):
        html = f"{datetime.now()}"
        return HttpResponse(html)


class randomView(View):
    def get(self, request):
        html = random()
        return HttpResponse(html)


class strHello(View):
    def get(self, request):
        html = "<h1>Hello, World</h1>"
        #html = "Hello, World"
        return HttpResponse(html)


class IndexView(View):
    def get(self, request):
        return render(request, 'other/index.html')


