import requests, math
from datetime import date

API_KEY = "c5da7f6762e05a36fc3391a80e90e947"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def convert_date(date):
    # YYYY - MM - DD
    months = [
        "index_0", "January", "February", "March", "April", "May", "June", 
        "July", "August", "September", "October", "November", "December"
    ]
    
    pieces_of_date = str(date).split("-")
    year = pieces_of_date[0]
    day = int(pieces_of_date[2])
    month = months[int(pieces_of_date[1])]
    return f"{month} {day}, {year}"

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
    
    city_data['temperature'] = f"{city_temp_f} °F"
    city_data['wind_speed'] = f"{city_wind_speed_mph} mph"
    
    return city_data

def search_for_city(cityinput): 
    city = cityinput.replace("_", " ").title()
    
    params = {
    "q": city,
    "appid": API_KEY,
    "units": "metric"
    }

    response = requests.get(BASE_URL, params=params)

    city_date = convert_date(date.today())

    if response.status_code == 200:
        data = response.json()
        city_temp = round(data['main']['temp'])
        city_weather_description = data['weather'][0]
        city_humidity = data['main']['humidity']
        city_wind_speed = data['wind']['speed']
        return {
            'valid' : True,
            'name' : city,
            'temperature' : f"{city_temp} °C", # celsius
            'temp_color' : get_temp_color(city_temp), # hex
            'weather_image' : get_weather_image(city_weather_description['main']),
            'weather' : city_weather_description['description'],
            'humidity' : city_humidity, # %
            'wind_speed' : f"{city_wind_speed} m/s", # m/s
            'date' : city_date, 
        }
        
    else:
        return {
            'valid' : False,
            'name' : None,
            'temperature' : None,  # celsius
            'temp_color' : None, # hex
            'weather_image' : None,
            'weather' : None,
            'humidity' : None, # %
            'wind_speed' : None, # m/s
            'date' : None,
        }