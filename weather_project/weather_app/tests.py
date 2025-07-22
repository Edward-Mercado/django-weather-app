from django.test import TestCase

# Create your tests here.
import json
with open("cities.json", "r") as file:
    cities = json.load(file)
    
print(cities)