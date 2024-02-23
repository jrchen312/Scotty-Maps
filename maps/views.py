from django.shortcuts import render
from django.http import HttpResponse

import requests
import os
from configparser import ConfigParser


def home(request):
    return render(request, "maps/home.html")

def building(request, building_name):
    print(building_name)
    return render(request, "maps/home_old.html")


def get_maps_script(request):
    CONFIG = ConfigParser()
    CONFIG.read("config.ini")

    google_maps_api_key = CONFIG.get("Maps", "Key")

    maps_url = 'https://maps.googleapis.com/maps/api/js?key={}&callback=initMap'.format(google_maps_api_key)
    response = requests.get(maps_url)

    # Important: Ensure proper content type for JavaScript
    return HttpResponse(response.content, content_type="application/javascript") 