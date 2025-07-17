from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
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
        
def change_url(request):
    template = loader.get_template('index.html')
    if request.method == "POST":
        user_input = request.POST.get('user_input')
        
        context = search_for_city(user_input)
        
        return redirect('change_url', parameter=user_input, context=context)
    return render(request, template)


def input_view(request): 
    if request.method == "POST":
        city_target = request.POST.get('user_input').replace(" ", "_")
        if city_target:
            return redirect('city', city_name = city_target)
    
    template = loader.get_template("blank.html")    
    return HttpResponse(template.render({}, request))

def city_view(request, city_name):
    context = search_for_city(city_name)
    print(context['temp_color'])
    if context['valid'] == True:
        template = loader.get_template('index.html')
        return HttpResponse(template.render(context, request))
    if context['valid'] == False:
        template = loader.get_template('blank.html')
        return HttpResponse(template.render(context, request))