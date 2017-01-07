import json
import requests

message = {'user_id': 1, 'floor_num': '5', 'building_num': '17', 'street_name': 'el helw st', 'longitude': '30.7846028',
           'latitude': '31.0025602'}
# message = json.dumps(message)
headers = {'Authorization': "627562626c6520617069206b6579"}
print('call endpoint now and update it')
res = requests.post('http://0.0.0.0:8080/getUserPhones', json=message, headers=headers)
print(res.text)
