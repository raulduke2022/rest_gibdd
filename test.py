import requests
import json

data = {
    'name': 'jack',
    'price': 5.2
}

new_data = json.dumps(data)

r = requests.post('https://testyoursite.ru:9002/items', data=new_data, )
print(r)