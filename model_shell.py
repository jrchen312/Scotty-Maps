
from maps.models import *

# HALL OF ARTS
hoa = Location(name="Hall of Arts", lat=40.4409058, lng=-79.94249)
hoa1 = Floor(location=hoa, name="Floor 1", img_path="hallofarts1.png", graph_path="300pxSquare_graph.json")

hoa.save()
hoa1.save()


# Hamerschlag Hall, Pittsburgh, PA 15213
hh = Location(name="Hamerschlag Hall", lat=40.4424073, lng=-79.9469101)
hh.save()

hh_test = Floor(location=hh, name="Test Square", img_path="300pxSquare.png", graph_path="300pxSquare_graph.json")
hh_test.save()

hh_A = Floor(location=hh, name="Floor A", img_path="hha.png", graph_path="hha_graph.json", 
                x_pixel_scale=175, y_pixel_scale=814, 
                x_pixel_offset=175, y_pixel_offset=136, 
                y_pixels_per_meter=18.555, x_pixels_per_meter=14.61)
                
hh_A.save()

# PHA hack (don't need anymore) 
from maps.models import *
hh = Location.objects.get(id=2)
ph_A = Floor(location=hoa, name="Porter A", img_path="pha.png", graph_path="hha_graph.json", x_pixel_scale=299, y_pixel_scale=23, x_pixel_offset=166, y_pixel_offset=634)
ph_A.save()


# Roberts 3rd floor. (don't need anymore either)
from maps.models import *
hh = Location.objects.get(id=2)
roberts_3 = Floor(location=hoa, name="Roberts 3", img_path="roberts3.png", graph_path="roberts3_graph.json", 
                  x_pixel_scale=385, y_pixel_scale=162, x_pixel_offset=767, y_pixel_offset=157,
                  y_pixels_per_meter=16.138, x_pixels_per_meter=15.955)
roberts_3.save()



# Wiegand Gym
from maps.models import *
wiegand = Location(name="CUC", lat=40.4433567, lng=-79.9419179)
wiegand.save()

wiegand_floor = Floor(location=wiegand, name="Wiegand Gym", img_path="wiegandv4.png", graph_path="wiegandv4_outer.json", 
                x_pixel_scale=1360-174, y_pixel_scale=1025-69, 
                x_pixel_offset=174, y_pixel_offset=69,
                x_pixels_per_meter=30.1, y_pixels_per_meter=30.1)
wiegand_floor.save()

# Wiegand Gym with navigation (outer)
wiegand_outer = Floor(location=wiegand, name="Wiegand Gym (Outer Navigation)", img_path="wiegandv4_outer.png", graph_path="wiegandv4_outer.json", 
                x_pixel_scale=1360-174, y_pixel_scale=1025-69, 
                x_pixel_offset=174, y_pixel_offset=69,
                x_pixels_per_meter=30.1, y_pixels_per_meter=30.1)
wiegand_outer.save()

# Wiegand Gym with navigation (inner)
wiegand_inner = Floor(location=wiegand, name="Wiegand Gym (Inner Navigation)", img_path="wiegandv4_inner.png", graph_path="wiegandv4_inner.json", 
                x_pixel_scale=1360-174, y_pixel_scale=1025-69, 
                x_pixel_offset=174, y_pixel_offset=69,
                x_pixels_per_meter=30.1, y_pixels_per_meter=30.1)
wiegand_inner.save()

# # Wiegand Gym, downscaled
# from maps.models import *
# wiegand = Location.objects.get(id=3)

# wiegand_floor_small = Floor(location=wiegand, name="Wiegand Gym Downscaled", img_path="wiegandv2.png", graph_path="wiegand_small_v2.json", #todo
#                 x_pixel_scale=730-137, y_pixel_scale=528-51, 
#                 x_pixel_offset=137, y_pixel_offset=51,
#                 x_pixels_per_meter=15.05, y_pixels_per_meter=15.05)
# wiegand_floor_small.save()

################################################################################
# NOTE: add new floors right above
################################################################################


# open up rooms.csv and import the rooms. 
import csv
from maps.models import *
room_floors = dict()

hh_A = Floor.objects.get(name = "Floor A")
reh3 = Floor.objects.get(name = "Roberts 3")
wiegand_inner = Floor.objects.get(name = "Wiegand Gym (Inner Navigation)")
wiegand_outer = Floor.objects.get(name = "Wiegand Gym (Outer Navigation)")

room_floors["hh_A"] = hh_A
room_floors["reh3"] = reh3
room_floors["inner"] = wiegand_inner
room_floors["outer"] = wiegand_outer

with open("reh3rooms.csv", "r") as file:
    csv_reader = csv.reader(file)
    for r in csv_reader:
        room = Room(floor=room_floors[r[0]], name=r[1], x_pos=int(r[2]), y_pos=int(r[3]))
        room.save()

with open("rooms.csv", "r") as file:
    csv_reader = csv.reader(file)
    for r in csv_reader:
        room = Room(floor=room_floors[r[0]], name=r[1], x_pos=int(r[2]), y_pos=int(r[3]))
        room.save()

with open("rooms_inner.csv", "r") as file:
    csv_reader = csv.reader(file)
    for r in csv_reader:
        room = Room(floor=room_floors[r[0]], name=r[1], x_pos=int(r[2]), y_pos=int(r[3]))
        room.save()

with open("rooms_outer.csv", "r") as file:
    csv_reader = csv.reader(file)
    for r in csv_reader:
        room = Room(floor=room_floors[r[0]], name=r[1], x_pos=int(r[2]), y_pos=int(r[3]))
        room.save()
