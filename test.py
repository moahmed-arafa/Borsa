__author__ = 'fantom'
import requests

message = {'stock_id': 1, 'value': 18.7}
headers = {'Authorization': "627562626c6520617069206b6579"}
print('call endpoint now and updateStockValve')
res = requests.post('http://0.0.0.0:8080/updateStockValve', json=message, headers=headers)
print(res.text)
