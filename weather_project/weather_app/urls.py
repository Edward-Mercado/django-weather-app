from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.main, name="main"), # homepage
    path("input/", views.input_view, name="input"), # view after inputting a target city
    path("input/random", views.random_view, name="random"), # view after selecting a random city
    path("search/<city_name>/<units>", views.city_view, name="city"), # resulting page after either input_view or random_view are called
]