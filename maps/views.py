from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt 
from django.urls import reverse
from .models import *

import requests
from configparser import ConfigParser

################################################################################
# HTML views
################################################################################

# Home View displaying a map
def home(request):
    return render(request, "maps/home.html")


# Floor View displaying a floor of a building. 
def floor(request, floor_id):
    context = dict()

    floor = Floor.objects.get(id=floor_id)

    context["img_file"] = floor.img_path
    context["floorId"] = floor_id
    context["tagId"] = "http_test" # should be connected to user acc
                                    # or for testing, the floor, 
    
    context["floorScaling"] = {
        "x_scaling": floor.x_pixel_scale,
        "y_scaling": floor.y_pixel_scale,
        "x_offset": floor.x_pixel_offset,
        "y_offset": floor.y_pixel_offset,
    }

    return render(request, "maps/floor.html", context=context)


################################################################################
# Asynchronous points
################################################################################

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

"""
Update the user location for a "floor". 

"""
@csrf_exempt
def update_user_location(request):
    if request.method == 'POST':
        data = request.POST
        # print(data)

        try:
            tag = Tag.objects.get(id=data["id"])
            # print("tag found")
        except:
            tag = Tag.objects.create(id=data["id"])
            print("created new tag")
        
        tag.x_pos = data["x_pos"]
        tag.y_pos = data["y_pos"]
        tag.rotation = data["rotation"]

        tag.floor = Floor.objects.get(id=data["floor"])

        tag.last_update_time = data["time"]

        tag.save()
        return JsonResponse({'message': 'Data received!'})
    else:
        return JsonResponse({'error': 'Only POST requests allowed.'})


USER_TAG = "http_test"
"""
For the "TEST
"""
def get_user_location(request):
    try:
        tag = Tag.objects.get(id=USER_TAG)
    except:
        return JsonResponse({'error': 'Tag ID not found.'})

    return JsonResponse({
        'x_pos': tag.x_pos,
        'y_pos': tag.y_pos,
        'rotation': tag.rotation,
        'time': tag.last_update_time,
    })
