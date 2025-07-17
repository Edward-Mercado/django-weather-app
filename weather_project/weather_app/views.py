from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .forms import MyForm

def main(request):
    template = loader.get_template('main.html')
    context = {}
    return HttpResponse(template.render(context, request))

def search(request):
    if request.method == "POST":