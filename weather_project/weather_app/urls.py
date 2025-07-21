from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("input/", views.input_view, name="input"),
    path("search/<city_name>/<units>", views.city_view, name="city"),
]