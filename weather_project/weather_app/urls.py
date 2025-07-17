from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("test-processing", views.search, name="search"),
]