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
        "#BDF6FF", "#35C3D9", "#61D7AC", "#5BE673",
        "#52D936", "#FDF670", "#FFB54C", "#FF8C7A", "#FA6969"
              ]
    color_index = math.floor(temp/5) # returns greatest integer < temp 

    if color_index > 7: # handles if we have temp > 40 dg celsius
        color_index = 8
    
    temp_color = colors[color_index]

    return temp_color

def get_weather_image(weather):
    pass
    
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
        city_weather_description = data['weather'][0]['description']
        city_humidity = data['main']['humidity']
        city_wind_speed = data['wind']['speed']
        return {
            'valid' : True,
            'name' : city,
            'temperature' : city_temp, # celsius
            'temp_color' : get_temp_color(city_temp), # hex
            'weather' : city_weather_description,
            'humidity' : city_humidity, # %
            'wind_speed' : city_wind_speed, # m/s
            'date' : city_date, 
        }
        
    else:
        return {
            'valid' : False,
            'name' : None,
            'temperature' : None,  # celsius
            'temp_color' : get_temp_color(city_temp), # hex
            'weather' : None,
            'humidity' : None, # %
            'wind_speed' : None, # m/s
            'date' : None,
        }