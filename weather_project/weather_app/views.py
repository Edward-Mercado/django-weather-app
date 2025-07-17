from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .search import search_for_city

def main(request):
    template = loader.get_template('main.html')
    context = {}
    return HttpResponse(template.render(context, request))

def search(request):
    if request.method == "POST":
        user_input = request.POST.get('user_input')
        
        context = search_for_city(user_input)
        
        if context['valid'] == True:
            template = loader.get_template('index.html')
            return HttpResponse(template.render(context, request))
        if context['valid'] == False:
            template = loader.get_template('blank.html')
            return HttpResponse(template.render(context, request))