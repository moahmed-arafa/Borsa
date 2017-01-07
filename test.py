__author__ = 'fantom'
import requests

message = {'first_name': 'Mohamed', 'last_name': 'Arafa', 'email': 'm.arafa1@gmail.com', 'password': 'Mohamed123'}
headers = {'Authorization': "627562626c6520617069206b6579"}
print('call endpoint now and signupUser')
res = requests.post('https://hyper-testing.herokuapp.com/signup', json=message, headers=headers)
print(res.text)

# message = {'user_id': 1, 'device_token': 1}
# print('call endpoint now and registerDevice')
# res = requests.post('https://hyper-testing.herokuapp.com/registerDevice', json=message, headers=headers)
# print(res.text)
#
# message = {'device_token': '627562626c6520617069206b6579'}
# print('call endpoint now and registerDeviceAnonymous')
# res = requests.post('https://hyper-testing.herokuapp.com/registerDeviceAnonymous', json=message, headers=headers)
# print(res.text)

message = {'email': 'gogogfoxx@live.com', 'password': 'Mohamed123'}
print('call endpoint now and login')
res = requests.post('https://hyper-testing.herokuapp.com/login', json=message, headers=headers)
print(res.text)

# message = {'user_id': 1, 'items': [{'item_id': 4062, 'quantity': 5}, {'item_id': 4063, 'quantity': 5},
#                                    {'item_id': 4435, 'quantity': 5}, {'item_id': 4436, 'quantity': 5}]}
# print('call endpoint now and makeOrder')
# res = requests.post('https://hyper-testing.herokuapp.com/makeOrder', json=message, headers=headers)
# print(res.text)
#
# message = {'user_id': 1}
# print('call endpoint now and getOrdersByUser')
# res = requests.post('https://hyper-testing.herokuapp.com/getOrdersByUser', json=message, headers=headers)
# print(res.text)
#
# message = {'user_id': 1, 'code': '02010', 'number': '62962830'}
# print('call endpoint now and update it')
# res = requests.post('https://hyper-testing.herokuapp.com/addPhone', json=message, headers=headers)
# print(res.text)
#
# message = {'user_id': 1, 'code': '02010', 'number': '62962830'}
# print('call endpoint now and update it')
# res = requests.post('https://hyper-testing.herokuapp.com/getUserPhones', json=message, headers=headers)
# print(res.text)
#
# message = {'user_id': 1, 'floor_num': '5', 'building_num': '17', 'street_name': 'el helw st', 'longitude': '30.7846028',
#            'latitude': '31.0025602'}
# print('call endpoint now and update it')
# res = requests.post('https://hyper-testing.herokuapp.com/addAddress', json=message, headers=headers)
# print(res.text)
#
# message = {'user_id': 1, 'floor_num': '5', 'building_num': '17', 'street_name': 'el helw st', 'longitude': '30.7846028',
#            'latitude': '31.0025602'}
# print('call endpoint now and update it')
# res = requests.post('https://hyper-testing.herokuapp.com/getUserAddress', json=message, headers=headers)
# print(res.text)
#
# message = {'user_id': 1, 'floor_num': '5', 'building_num': '17', 'street_name': 'el helw st', 'longitude': '30.7846028',
#            'latitude': '31.0025602'}
# print('call endpoint now and update it')
# res = requests.post('https://hyper-testing.herokuapp.com/getUserPhones', json=message, headers=headers)
# print(res.text)
