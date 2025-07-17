import requests
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
            'weather' : None,
            'humidity' : None, # %
            'wind_speed' : None, # m/s
            'date' : None,
        }
        
