from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('' , home , name="home"),
    path('api/hotels' , api_hotels),
    path('api/hotel_search' , hotel_search)
]
