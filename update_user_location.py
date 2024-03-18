import time
import requests
import random


url = 'http://127.0.0.1:8000/update_user_location'
url = 'http://3.90.105.209:8000/update_user_location'




for _ in range(1000):
    time.sleep(1)

    data = {
        'id': 'http_test',          # id of the tag device (keep as "http_test")
        # 'x_pos': 0.3406, 
        # 'y_pos': 0.2959,
        'x_pos': random.random(),   # x position in [0, 1]
        'y_pos': random.random(),   # y position in [0, 1]
        'floor': 1,                 # "floor id" (keep as "1" for test square)

        'time': time.time(),        # time for benchmarking purposes. 
    }


    response = requests.post(url, data=data)

    if response.status_code == 200:
        print('User location updated successfully!')
    else:
        print('An error occurred:', response.status_code, response.text)
