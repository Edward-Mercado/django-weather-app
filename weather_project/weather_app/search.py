import requests, math, datetime
from datetime import date

API_KEY = "c5da7f6762e05a36fc3391a80e90e947"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def snake_case(text=str, reverse=bool, title=bool): # this function converts regular text to snake cased ones and in reverse
    if reverse==False: # if we arent reversing it, standard snake casing
        return text.replace(" ", "_").lower()
    else:
        if title==True: # title boolean is if you want to cap the first letter of each word
            return text.replace("_", " ").title()
        else:
            return text.replace("_", " ")
        
def convert_date(date, format):
    # YYYY - MM - DD, formatting of the date that date.today() gives you
    months = [
        "January", "February", "March", "April", "May", "June", 
        "July", "August", "September", "October", "November", "December"
    ]
    
    pieces_of_date = str(date).split("-") # split the date across each piece of it
    year = pieces_of_date[0]
    day = int(pieces_of_date[2])
    suffixlist_st = [1, 21, 31]
    suffixlist_nd= [2, 22]
    suffixlist_rd = [3, 23]

    if day in suffixlist_st: # suffix maker
        suffix = "st"
    elif day in suffixlist_nd:
        suffix = "nd"
    elif day in suffixlist_rd:
        suffix = "rd"
    else:
        suffix = "th"
    
    month = months[int(pieces_of_date[1])-1] # determine which month to pull from the list based on month number
    if format== "mmddyyyy": # the correct format
        return f"{month} {day}, {year}"
    if format== "wrong": # the other format
        return f"the {day}{suffix} of {month}, {year}"

def get_formatted_time(units):
    date_and_time = str(datetime.datetime.now())

    current_time = date_and_time.split(" ")[1] # returns just the time piece (not the date)
    rounded_time = current_time.split(".")[0] # returns the time without miliseconds
    pieces_of_time = rounded_time.split(":") # returns the time as a list of [hour, minute, second]
    if units == "imperial": # this will be in the AM/PM format
        day_half = "AM" # default AM
        
        if int(pieces_of_time[0]) > 12: # if we are in the second half of the day, convert to PM
            pieces_of_time[0] = str(int(pieces_of_time) - 12)
            day_half = "PM"
        elif int(pieces_of_time[0]) == 12:
            day_half = "PM"
        elif int(pieces_of_time[0]) == 0:
            pieces_of_time[0] == 12
            
        return f"{pieces_of_time[0]}:{pieces_of_time[1]} {day_half} (EST)"
    else: # this will be in the 24 hour day format
        return f"{pieces_of_time[0]}:{pieces_of_time[1]} (EST)"

def get_temp_color(temp):
    colors = [
        "#FBFEFF", "#BDF6FF", "#35C3D9", "#61D7AC", "#8DFFDD",
        "#FFFEB6", "#FDF670", "#FFB54C", "#FF8C7A", "#FA6969",
              ]
    color_index = math.floor(temp/5) # floor function returns greatest integer < temp 
    # divide by 5 so each increment of 5 dg celsius moves you up one "hotter" color

    if color_index < 0: # negative numbers will return index 0 when determining temp color
        color_index = -1
    
    if color_index > 7: # handles if we have temp > 40 dg celsius
        color_index = 8
    
    temp_color = colors[color_index + 1] # pulling the color from the list

    return temp_color

def get_weather_image(weather):
    weather_name = weather.lower()

    possible_image_values = { # urls for the types of images that demonstrate the weather
        "sun" : "images/sunny.png",
        "rain" : "images/rain.png",
        "cloud" : "images/cloud.png",
        "storm" : "images/storm.png",
        "snow" : "images/snow.webp",
        "clear" : "images/clear.png",
    } 
    # the weather description of the api will always give at least one of these phrases from the key, so i categorized them this way
    
    image_value = None
    for key in possible_image_values.keys(): # get the keys from the dictionary
        if key in weather_name: # check if the name of the key is in the name of the weather (ex. is "cloud" in "partially cloudy")
            image_value = possible_image_values[key] # if so grab the image url
            
    if image_value == None: # make it return SOMETHING (though my categorization already covers everything)
        image_value = '0'
        
    return image_value

def convert_to_imperial(city_data):
    city_temp_c = int(city_data['temperature'].strip(" °C")) # return the city temperature in celsius as an integer
    city_temp_f = int((city_temp_c*18) + 320) / 10 # formula to get the fahrenheit temperature rounded to the tenth
    
    city_wind_speed_mps = float(city_data['wind_speed'].strip(" m/s")) # get the windspeed as an integer without the unit 
    city_wind_speed_mph = (int(city_wind_speed_mps*22.3694) / 10) # rough conversion rate of meters per second to miles per hour
    
    city_data['temperature'] = f"{int(city_temp_f)} °F" # changing the temperature value to the fahrenheit one
    city_data['wind_speed'] = f"{city_wind_speed_mph} mph" # changing the windspeed value to the mph one
    city_data['time'] = get_formatted_time("imperial") # format the time to the AM/PM schedule
    city_data['units'] = "imperial" # these are the units we are using (it helps the main function know how to convert the units)
    city_data['reverse_units'] = "metric" # target units for when the user wants to return it back to metric
    
    return city_data

def check_search_validity(cityinput):
    city = snake_case(cityinput, True, True) # ensure that the api input is in valid formatting (ex. new_york_city -> New York City)
    response = requests.get(BASE_URL, params={ # make request to the api
    "q": city,
    "appid": API_KEY,
    "units": "metric"
    })

    return response.status_code == 200 # if the response is valid then it will return true

def get_humidity_descriptor(humidity): # returns a short description for the humidity
    humidity_descriptors = [ # links the humidity value to the flavor text
        {
            'minimum': 0,
            'maximum': 20,
            'description': "very dry",
        },
        {
            'minimum': 21,
            'maximum': 40,
            'description': "a tad dry",
        },
        {
            'minimum': 41,
            'maximum': 60,
            'description': "comfortable",
        },
        {
            'minimum': 61,
            'maximum': 80,
            'description': "pretty humid",
        },
        {
            'minimum': 81,
            'maximum': 94,
            'description': "very humid",
        },
        {
            'minimum': 95,
            'maximum' : 100,
            'description' : 'like a sauna',
        },
    ]
    
    for humidity_descriptor in humidity_descriptors:
        humidity = int(humidity) # round the humdity value (im pretty sure it already returns and integer but to be safe and im too lazy to check)
        if humidity >= humidity_descriptor['minimum'] and humidity <= humidity_descriptor['maximum']: # if it is in the range set
            return humidity_descriptor['description'] # return its description
    
    return "invalid humidity value" # if for some reason my code doesnt work return something

def search_for_city(cityinput): # actual search function that calls the api
    snake_cased_name = snake_case(cityinput, False, False)
    city = snake_case(snake_cased_name, True, True) # ensure that the api input is in valid formatting (ex. new_york_city -> New York City)
    
    params = { # api parameters
    "q": city,
    "appid": API_KEY,
    "units": "metric"
    }

    response = requests.get(BASE_URL, params=params) # call api

    city_date = convert_date(date.today(), "wrong") # get the date in the ddmmyyyy (wrong) format

    if response.status_code == 200: # if our search is valid,
        data = response.json() # get all the data
        # getting all the variables
        city_temp = round(data['main']['temp'])
        city_weather_description = data['weather'][0]
        city_humidity = data['main']['humidity']
        city_wind_speed = data['wind']['speed']
        # return a dictionary we can use as context to load the HTML file
        return {
            'valid' : True,
            "snake_cased_name": snake_cased_name,
            'name' : city,
            'temperature' : f"{city_temp} °C", # celsius
            'temp_color' : get_temp_color(city_temp), # hex
            'weather_image' : get_weather_image(city_weather_description['main']),
            'weather' : city_weather_description['description'],
            'humidity' : city_humidity, # %]
            'humidity_descriptor' : get_humidity_descriptor(city_humidity),
            'wind_speed' : f"{city_wind_speed} m/s", # m/s
            'date' : city_date, 
            "time" : get_formatted_time("metric"),
            "units": "metric",
            "reverse_units": "imperial",
        }
        
    else: # if the response isnt valid
        return { # return a random empty dictionary
            'valid' : False, # valid = False here, so it will load our blank.html
            "snake_cased_name": None,
            'name' : None,
            'temperature' : None,  # celsius
            'temp_color' : None, # hex
            'weather_image' : None,
            'weather' : None,
            'humidity' : None, # %
            'wind_speed' : None, # m/s
            'date' : None,
            "units": "metric",
            "reverse_units": "imperial",
        }