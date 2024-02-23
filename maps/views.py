from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, "maps/home.html")

def building(request, building_name):
    print(building_name)
    return render(request, "maps/home_old.html")