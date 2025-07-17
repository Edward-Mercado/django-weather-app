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
        template = loader.get_template('index.html')
        search_for_city()
        
        
        context = {'user_input' : user_input}
        
        return HttpResponse(template.render(context, request))
    
    return HttpResponse('damn')