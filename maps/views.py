from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from .models import *

import requests
import os
from configparser import ConfigParser


def home(request):
    return render(request, "maps/home.html")


def building(request, building_name):
    print(building_name)
    return render(request, "maps/home_old.html")


def floor(request, floor_id):
    context=dict()

    floor = Floor.objects.get(id=floor_id)
    
    context["img_file"] = floor.img_path

    return render(request, "maps/floor.html", context=context)

# Proxy point to load the google maps API from the server. 
def get_maps_script(request):
    CONFIG = ConfigParser()
    CONFIG.read("config.ini")

    google_maps_api_key = CONFIG.get("Maps", "Key")

    maps_url = f'https://maps.googleapis.com/maps/api/js?key={google_maps_api_key}&callback=initMap'
    response = requests.get(maps_url)

    # Important: Ensure proper content type for JavaScript
    return HttpResponse(response.content, content_type="application/javascript") 


# AJAX point to get the map pin locations from the server. 
# Let the client build the HTML necessary. 
def get_map_pins(request):

    info = []
    for location in Location.objects.all():
        i = dict()

        i["name"] = location.name
        i["lat"] = location.lat
        i["lng"] = location.lng

        floors = []
        for floor in location.floors.all():
            f = dict()
            f["name"] = floor.name
            f["img_path"] = reverse("floor", args=[floor.id])
            floors.append(f)
        i["floors"] = floors

        info.append(i)
    
    return JsonResponse(info, safe=False, content_type="application/javascript")
