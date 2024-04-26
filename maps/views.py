from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt 
from django.urls import reverse
from .models import *
from .a_star_alg import navigation_directions
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import SpecialUserCreationForm, ProfileEditForm

import time
import requests
from configparser import ConfigParser

################################################################################
# HTML views
################################################################################

# Home View displaying a map
@login_required
def home(request):
    return render(request, "maps/home.html")


# Floor View displaying a floor of a building. 
@login_required
def floor(request, floor_id):
    context = dict()
    user_profile = request.user.profile

    if ((not user_profile.tag_id) or (len(user_profile.tag_id) < 2)):
        return redirect(profile)

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

        "y_pixels_per_meter": floor.y_pixels_per_meter,
        "x_pixels_per_meter": floor.x_pixels_per_meter,
    }

    return render(request, "maps/floor.html", context=context)


# profile view
@login_required
def profile(request):
    user = request.user
    profile = user.profile

    prof_form = ProfileEditForm(initial={
        "name": profile.name,
        "tag_id": profile.tag_id,
    })

    if (request.method == "POST"):
        form = ProfileEditForm(request.POST)
        if (form.is_valid()):

            profile.name = form.cleaned_data["name"]
            profile.tag_id = form.cleaned_data["tag_id"]
            profile.save()
            prof_form = ProfileEditForm(initial={
                "name": profile.name,
                "tag_id": profile.tag_id,
            })
        else:
            prof_form = form;

    context = {
        "user": user,
        "profile": profile,
        "form": prof_form,
        "tag_id_wrong": (not profile.tag_id) or (len(profile.tag_id) < 2)
    }
    return render(request, "maps/profile.html", context=context)


# sign up
def sign_up(request):
    if (request.method == "POST"):
        form = SpecialUserCreationForm(request.POST)
        if (form.is_valid()):
            # create the user
            user, profile = form.save()

            # create the associated profile
            # profile = Profile(user=user, 
            #                   tag_id="")
            login(request=request, user=user)
            return redirect(home)
        else:
            return render(request, "maps/sign_up.html", context={
                "form": form,
                "next": reverse("home"),
            })
    return render(request, "maps/sign_up.html", context={
        "form": SpecialUserCreationForm(),
        "next": reverse("home"),
    })

def logout_user(request):
    logout(request)
    return redirect(home)

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
# import os
def update_navigation_directions(request):
    time_0 = time.time()
    if request.method != 'POST':
        return JsonResponse({'error': "only post requests allowed"})
    
    data = request.POST
    # print(data)

    # print(os.listdir())
    floor = Floor.objects.get(id = data["floor_id"])

    room = floor.rooms.get(name = data["room_name"])
    # room = Room.objects.get(name = data["room_name"])
    # floor = room.floor
    

    graph_path = f"./maps/static/maps/{floor.graph_path}"

    user_row = int(float(data["user_y"]))
    user_col = int(float(data["user_x"]))

    dest_row = room.y_pos
    dest_col = room.x_pos

    paths, txt, icon = navigation_directions(graph_path, user_row, user_col, dest_row, dest_col)
    
    time_1 = time.time()
    print(f"time_taken({time_1-time_0})")
    print(paths, txt)

    return JsonResponse({
        'directions': paths,
        'instruction': txt,
        'icon': icon,
    })

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
