from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt 
from django.urls import reverse
from .models import *
from .a_star_alg import navigation_directions

import time
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
    
    # include the rooms of the floor. 
    context["rooms"] = floor.rooms.all().order_by('name')

    # used for the client to hold information regarding the floor to display
    # the user's position. 
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
Given the position of a user, provide the directions necessary to get to a room

The client will provide these directions as a pixel location.
To use them in our graph, we will convert them into the graph's row and col. 
"""
import os
def update_navigation_directions(request):
    time_0 = time.time()
    if request.method != 'POST':
        return JsonResponse({'error': "only post requests allowed"})
    
    data = request.POST
    print(data)

    print(os.listdir())
    floor = Floor.objects.get(id = data["floor_id"])

    room = floor.rooms.get(name = data["room_name"])
    # room = Room.objects.get(name = data["room_name"])
    # floor = room.floor
    

    graph_path = f"./maps/static/maps/{floor.graph_path}"

    user_row = int(float(data["user_y"]))
    user_col = int(float(data["user_x"]))

    dest_row = room.y_pos
    dest_col = room.x_pos

    paths = navigation_directions(graph_path, user_row, user_col, dest_row, dest_col)
    
    time_1 = time.time()
    print(f"time_taken({time_1-time_0})")
    print(paths)
    return JsonResponse({'directions': paths})

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
