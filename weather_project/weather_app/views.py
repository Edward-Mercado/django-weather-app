from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .search import convert_to_imperial
from .search import search_for_city
from .search import convert_date
from datetime import date
import json
import random
import os

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
        units = request.POST.get('unit_type')
        if units == "on":
            units = "imperial"
        else:
            units = "metric"
        if search_for_city(city_target)['valid'] == True:
            return redirect('city', city_name = city_target, units=units)
        else:
            return redirect('city', city_name = "invalid", units = "invalid")
    
    template = loader.get_template("blank.html")    
    return HttpResponse(template.render({}, request))

def random_view(request):
    current_dir = os.path.dirname(__file__)
    json_path = os.path.join(current_dir, 'cities.json')

    with open(json_path, 'r', encoding='utf-8') as f:
        cities = json.load(f)    
    
    city_target = cities[random.randint(0, 295)].lower()
        
    if search_for_city(city_target)['valid'] == True:
        return redirect('city', city_name = city_target, units="metric")
    else:
        return redirect('city', city_name = "invalid", units = "invalid")

def city_view(request, city_name, units):
    prep_context = search_for_city(city_name)
    
    if prep_context['valid'] == True:
        template = loader.get_template('index.html')
        context = prep_context
        if units == "imperial": # shush, please
            context = convert_to_imperial(prep_context)
            context['date'] = convert_date(date.today(), "mmddyyyy")

        return HttpResponse(template.render(context, request))
    elif prep_context['valid'] == False:
        template = loader.get_template('blank.html')
        context = prep_context
        return HttpResponse(template.render(context, request))