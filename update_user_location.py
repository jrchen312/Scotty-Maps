import time
import requests
import random


url = 'http://127.0.0.1:8000/update_user_location'
url = 'http://3.90.105.209:8000/update_user_location'




for _ in range(1000):
    time.sleep(1)

    data = {
        'id': 'http_test', 
        # 'x_pos': 0.3406, 
        # 'y_pos': 0.2959,
        'x_pos': random.random(), 
        'y_pos': random.random(),
        "floor": 1
    }


    response = requests.post(url, data=data)

    if response.status_code == 200:
        print('User location updated successfully!')
    else:
        print('An error occurred:', response.status_code, response.text)
