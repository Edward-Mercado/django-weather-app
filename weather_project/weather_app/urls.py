from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("/<city_name>", views.search, name="city"),
]