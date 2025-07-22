import requests, math, datetime
from datetime import date

API_KEY = "c5da7f6762e05a36fc3391a80e90e947"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def snake_case(text=str, reverse=bool, title=bool):
    if reverse==False:
        return text.replace(" ", "_").lower()
    else:
        if title==True:
            return text.replace("_", " ").title()
        else:
            return text.replace("_", " ")
        
def convert_date(date, format):
    # YYYY - MM - DD
    months = [
        "January", "February", "March", "April", "May", "June", 
        "July", "August", "September", "October", "November", "December"
    ]
    
    pieces_of_date = str(date).split("-")
    year = pieces_of_date[0]
    day = int(pieces_of_date[2])
    suffixlist_st = [1, 21, 31]
    suffixlist_nd= [2, 22]
    suffixlist_rd = [3, 23]

    if day in suffixlist_st:
        suffix = "st"
    elif day in suffixlist_nd:
        suffix = "nd"
    elif day in suffixlist_rd:
        suffix = "rd"
    else:
        suffix = "th"
    
    month = months[int(pieces_of_date[1])-1]
    if format== "mmddyyyy":
        return f"{month} {day}, {year}"
    if format== "wrong":
        return f"the {day}{suffix} of {month}, {year}"

def get_formatted_time(units):
    date_and_time = str(datetime.datetime.now())

    current_time = date_and_time.split(" ")[1] # returns just the time piece (not the date)
    rounded_time = current_time.split(".")[0] # returns the time without miliseconds
    pieces_of_time = rounded_time.split(":") # returns the time as a list of [hour, minute, second]
    if units == "imperial":
        day_half = "AM"
        
        if int(pieces_of_time[0]) > 12:
            pieces_of_time[0] = str(int(pieces_of_time) - 12)
            day_half = "PM"
        elif int(pieces_of_time[0]) == 12:
            day_half = "PM"
        elif int(pieces_of_time[0]) == 0:
            pieces_of_time[0] == 12
            
        return f"{pieces_of_time[0]}:{pieces_of_time[1]} {day_half} (EST)"
    else:
        return f"{pieces_of_time[0]}:{pieces_of_time[1]} (EST)"

def get_temp_color(temp):
    colors = [
        "#FBFEFF", "#BDF6FF", "#35C3D9", "#61D7AC", "#8DFFDD",
        "#FFFEB6", "#FDF670", "#FFB54C", "#FF8C7A", "#FA6969",
              ]
    color_index = math.floor(temp/5) # returns greatest integer < temp 

    if color_index < 0:
        color_index = -1
    
    if color_index > 7: # handles if we have temp > 40 dg celsius
        color_index = 8
    
    temp_color = colors[color_index + 1]

    return temp_color

def get_weather_image(weather):
    weather_name = weather.lower()

    possible_image_values = {
        "sun" : "images/sunny.png",
        "rain" : "images/rain.png",
        "cloud" : "images/cloud.png",
        "storm" : "images/storm.png",
        "snow" : "images/snow.webp",
        "clear" : "images/clear.png",
    }
    
    image_value = None
    for key in possible_image_values.keys():
        if key in weather_name:
            image_value = possible_image_values[key]
            
    if image_value == None:
        image_value = '0'
        
    return image_value

def convert_to_imperial(city_data):
    city_temp_c = int(city_data['temperature'].strip(" °C"))
    city_temp_f = int((city_temp_c*18) + 320) / 10
    
    city_wind_speed_mps = float(city_data['wind_speed'].strip(" m/s"))
    city_wind_speed_mph = (int(city_wind_speed_mps*22.3694) / 10)
    
    city_data['temperature'] = f"{int(city_temp_f)} °F"
    city_data['wind_speed'] = f"{city_wind_speed_mph} mph"
    city_data['time'] = get_formatted_time("imperial")
    city_data['units'] = "imperial"
    city_data['reverse_units'] = "metric"
    
    return city_data

def check_search_validity(cityinput):
    city = cityinput.replace("_", " ").title()

    response = requests.get(BASE_URL, params={
    "q": city,
    "appid": API_KEY,
    "units": "metric"
    })

    if response.status_code == 200:
        return True
    else:
        return False

def search_for_city(cityinput): 
    snake_cased_name = snake_case(cityinput, False, False)
    city = cityinput.replace("_", " ").title()
    
    params = {
    "q": city,
    "appid": API_KEY,
    "units": "metric"
    }

    response = requests.get(BASE_URL, params=params)

    city_date = convert_date(date.today(), "wrong")

    if response.status_code == 200:
        data = response.json()
        city_temp = round(data['main']['temp'])
        city_weather_description = data['weather'][0]
        city_humidity = data['main']['humidity']
        city_wind_speed = data['wind']['speed']
        return {
            'valid' : True,
            "snake_cased_name": snake_cased_name,
            'name' : city,
            'temperature' : f"{city_temp} °C", # celsius
            'temp_color' : get_temp_color(city_temp), # hex
            'weather_image' : get_weather_image(city_weather_description['main']),
            'weather' : city_weather_description['description'],
            'humidity' : city_humidity, # %
            'wind_speed' : f"{city_wind_speed} m/s", # m/s
            'date' : city_date, 
            "time" : get_formatted_time("metric"),
            "units": "metric",
            "reverse_units": "imperial",
        }
        
    else:
        return {
            'valid' : False,
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