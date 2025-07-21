from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .search import convert_to_imperial
from .search import search_for_city
from .search import convert_date
from datetime import date
import random

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
    cities = [
    "Tokyo", "Brazil", "Cairo", "Germany", "Nairobi", "Mexico City", "Thailand", "Helsinki", "Lima", "Canada",
    "Istanbul", "Vietnam", "Jakarta", "Morocco", "Manila", "France", "Buenos Aires", "Norway", "Seoul", "Ethiopia",
    "Kuala Lumpur", "Italy", "Baghdad", "Russia", "Santiago", "Kenya", "Amsterdam", "India", "Riyadh", "Portugal",
    "Beijing", "Spain", "Caracas", "Peru", "Athens", "Philippines", "New York", "Tehran", "Denmark",
    "Stockholm", "Pakistan", "Bangkok", "Colombia", "Oslo", "Algeria", "Addis Ababa", "Netherlands", "Doha", "Ukraine",
    "Los Angeles", "Saudi Arabia", "Warsaw", "Hungary", "Hanoi", "China", "Kigali", "Sweden", "Abu Dhabi", "Malaysia",
    "Lagos", "Poland", "Zurich", "Turkey", "Montreal", "Indonesia", "Tunis", "Serbia", "Toronto", "Iran",
    "Casablanca", "Croatia", "Dubai", "Finland", "Berlin", "Romania", "Vienna", "Sudan", "Barcelona", "Ireland",
    "Luanda", "Switzerland", "Munich", "Belgium", "Kinshasa", "Czech Republic", "Prague", "Slovakia", "Ankara", "Moroni",
    "Sofia", "New Delhi", "Zagreb", "Greece", "Cape Town", "Mozambique", "Lusaka", "Slovenia", "Reykjavik", "Cameroon",
    "Doha", "Estonia", "Panama City", "Ecuador", "Brussels", "Nicaragua", "Kampala", "Guatemala", "San Salvador", "Iceland",
    "Kabul", "Kuwait City", "Kuwait", "La Paz", "Bolivia", "Caracas", "Samoa", "Bucharest", "Belgrade", "Latvia",
    "Yerevan", "Georgia", "Quito", "Libya", "Vilnius", "Lithuania", "Skopje", "North Macedonia", "Tbilisi", "Malta",
    "Ashgabat", "Turkmenistan", "Bratislava", "Kosovo", "Podgorica", "Montenegro", "Monaco", "Andorra", "San Marino", "Liechtenstein",
    "Suva", "Fiji", "Valletta", "Nicosia", "Cyprus", "Muscat", "Oman", "Manama", "Bahrain", "Kathmandu",
    "Nepal", "Bhutan", "Thimphu", "Ulaanbaatar", "Mongolia", "Honiara", "Solomon Islands", "Port Vila", "Vanuatu", "Majuro",
    "Marshall Islands", "Palikir", "Micronesia", "Funafuti", "Tuvalu", "Nuku'alofa", "Tonga", "Port Moresby", "Papua New Guinea", "Apia",
    "Bangui", "Central African Republic", "Bamako", "Mali", "Ouagadougou", "Burkina Faso", "Freetown", "Sierra Leone", "Monrovia", "Liberia",
    "Gaborone", "Botswana", "Maseru", "Lesotho", "Bissau", "Guinea-Bissau", "Lilongwe", "Malawi", "Juba", "South Sudan",
    "Asmara", "Eritrea", "Djibouti", "Djibouti", "Mogadishu", "Somalia", "N'Djamena", "Chad", "Niamey", "Niger",
    "Yamoussoukro", "Ivory Coast", "Accra", "Ghana", "Lomé", "Togo", "Cotonou", "Benin", "Libreville", "Gabon",
    "Malabo", "Equatorial Guinea", "Brazzaville", "Congo", "Kigali", "Rwanda", "Bujumbura", "Burundi", "Maputo", "Mozambique",
    "Harare", "Zimbabwe", "Windhoek", "Namibia", "Pretoria", "Gaza", "Palestine", "Jerusalem", "Israel",
    "Amman", "Jordan", "Beirut", "Lebanon", "Damascus", "Syria", "Tashkent", "Uzbekistan", "Bishkek", "Kyrgyzstan",
    "Dushanbe", "Tajikistan", "Nur-Sultan", "Kazakhstan", "Pyongyang", "North Korea", "Seoul", "Taipei", "Taiwan",
    "Tokyo", "Japan", "Canberra", "Australia", "Wellington", "New Zealand", "Sucre", "Bolivia", "Asunción", "Paraguay",
    "Montevideo", "Uruguay", "Paramaribo", "Suriname", "Georgetown", "Guyana", "Belmopan", "Belize", "Port-au-Prince", "Haiti",
    "Kingston", "Jamaica", "Havana", "Cuba", "Santo Domingo", "Dominican Republic", "San Juan", "Puerto Rico", "Panama City", "Panama",
    "San José", "Costa Rica", "Tegucigalpa", "Honduras", "Managua", "Nicaragua", "Port of Spain", "Trinidad and Tobago", "Castries", "Saint Lucia",
    "Bridgetown", "Barbados", "Roseau", "Dominica", "Basseterre",  "St. George's", "Grenada", "Kingstown", "Saint Vincent and the Grenadines",
    "Victoria", "Seychelles", "Port Louis", "Mauritius", "Antananarivo", "Madagascar", "Moroni", "Comoros", "São Tomé", "São Tomé and Príncipe",
    "Colombo", "Sri Lanka", "Male", "Maldives", "Singapore", "Singapore", "Honiara", "Solomon Islands", "Tarawa", "Kiribati"
]
        
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