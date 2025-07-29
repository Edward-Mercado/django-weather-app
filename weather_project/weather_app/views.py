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

def main(request): # loads the homepage
    template = loader.get_template('main.html')
    context = {} # no context required
    return HttpResponse(template.render(context, request))

def input_view(request):  # this will redirect you to the url named city (which takes you to the city_view function)
    if request.method == "POST": # if there is user input
        city_target = request.POST.get('user_input').replace(" ", "_") # grab the user input and snake case it
        units = request.POST.get('unit_type') # this is if the imperial checkbox is turned on
        if units == "on": # checkbox filled
            units = "imperial"
        else:
            units = "metric"
        if search_for_city(city_target)['valid'] == True: # get the response from the api to see if we can load the city details
            return redirect('city', city_name = city_target, units=units)
        else:
            return redirect('city', city_name = "invalid", units = "invalid")
    
    template = loader.get_template("blank.html")    
    return HttpResponse(template.render({}, request))

def random_view(request): # loads a random city
    current_dir = os.path.dirname(__file__)
    json_path = os.path.join(current_dir, 'cities.json') # get the file name for cities.json

    with open(json_path, 'r', encoding='utf-8') as f:
        cities = json.load(f) # get our json file of 300ish random locations    
    
    city_target = cities[random.randint(0, 295)].lower() # get a random city and lower case it
        
    if search_for_city(city_target)['valid'] == True: # get the response from the api to see if we can load the city 
        # details (which we should but just in case chatgpt gave me a faulty list i dont want to have an error)
        return redirect('city', city_name = city_target, units="metric")
    else:
        return redirect('city', city_name = "invalid", units = "invalid")

def city_view(request, city_name, units): # the random_view and input_view functions will redirect the user to this function, that actually loads the page
    prep_context = search_for_city(city_name) # prep the context  with metric units 
    
    if prep_context['valid'] == True: # if its valid
        template = loader.get_template('index.html')
        context = prep_context # set our actual context to our prepped context first
        if units == "imperial": # if we want imperial units 
            context = convert_to_imperial(prep_context) # change the context to our prepped context after imperial conversion
            context['date'] = convert_date(date.today(), "mmddyyyy") # and change the date formatting
            
        return HttpResponse(template.render(context, request)) # load the page
    
    elif prep_context['valid'] == False: # if its invalid
        template = loader.get_template('blank.html') # load our blank.html error file
        context = prep_context # we don't actually *need* the context here this is so we can run the function without errors
        return HttpResponse(template.render(context, request)) # load the page