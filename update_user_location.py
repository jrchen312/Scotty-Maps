"""
How to use:

Go to http://3.90.105.209:8000/floor/2
Run this script. The user position should change. 
"""


import time
import requests
import random

# WEBAPP_URL = 'http://127.0.0.1:8000/update_user_location'

# url of webserver
WEBAPP_URL = 'http://3.90.105.209:8000/update_user_location'


# these constants should not be changed. 
TAG_ID = "http_test"
FLOOR_ID = 1


# general form of function: 
def update_user_position():
    # Mark the start time of the process. 
    initial_time = time.time()

    # Get the user position
    time.sleep(0.1)       # emulate the user position taking some time to finish
    x_pos = random.random()
    y_pos = random.random()

    # Compile data dictionary. All fields are mandatory. 
    data = {
        'id': TAG_ID,               # id of the tag device (keep as "http_test")
        'x_pos': x_pos,             # x position in [0, 1]
        'y_pos': y_pos,             # y position in [0, 1]
        'floor': FLOOR_ID,          # "floor id" (keep as "1" for test square)
        'time': initial_time,       # time for benchmarking purposes. 
    }

    # Send the response to the server
    response = requests.post(WEBAPP_URL, data=data)
    if response.status_code == 200:
        print('User location updated successfully!')
    else:
        print('An error occurred:', response.status_code, response.text)


for _ in range(1000):
    time.sleep(0.4)
    update_user_position()

    

