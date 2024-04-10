"""
How to use:

Go to http://3.90.105.209:8000/floor/2
Run this script. The user position should change. 
"""


import time
import requests
import random
import websockets
import json
import asyncio

# Do not change
TAG_ID = "http_test"

# Theoretically the tag device is able to figure out which floor it is in, but
# just hard code it...
# 1: Hall of Arts 1
# 2: Test Square
# 3: Hamerschlag A
# 4: porter hall A
FLOOR_ID = 3

WEBAPP_URI = f"ws://localhost:8000/ws/get_location/{FLOOR_ID}/{TAG_ID}/"

# # url of webserver
# WEBAPP_URI = f"ws://3.90.105.209:8000/ws/get_location/{FLOOR_ID}/{TAG_ID}/"


# send update
async def update_user_position(websocket, initial_time, x_pos, y_pos, rotation):
    # Compile data dictionary. All fields are mandatory. 
    data = {
        'type': 'update',
        'tag_id': TAG_ID,           # id of the tag device (keep as "http_test")
        'x_pos': x_pos,             # x position in [0, 1]
        'y_pos': y_pos,             # y position in [0, 1]
        'rotation': rotation,       # rotation, in degrees. 
        'floor': FLOOR_ID,          # "floor id" (keep as "1" for test square)
        'time': initial_time,       # time for benchmarking purposes. 
    }

    await websocket.send(json.dumps(data))
    _ = await websocket.recv()


"""
Main sequence of events to send to the server
If the device gets disconnected from the websocket, just try connecting again.
"""
async def main():
    while True:
        try:
            async with websockets.connect(WEBAPP_URI) as websocket:
                while True:
                    x_pos = min(max(random.random(), 0), 1) # change me
                    y_pos = min(max(random.random(), 0), 1) # change me
                    rotation = random.random()*360          # change me

                    # for i in range(10):
                    time1 = time.time()

                    await update_user_position(websocket, time1, x_pos, y_pos, rotation)
                    time2 = time.time()

                    print(f"Time required: {time2-time1}")
                        # time.sleep(1)

        except Exception as e:
            print(e)
            time.sleep(2)
    

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())

        

