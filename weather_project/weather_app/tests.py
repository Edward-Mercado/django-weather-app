from django.test import TestCase

# Create your tests here.

import datetime

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
    
print(get_formatted_time("metric"))