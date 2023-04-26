import requests

r = requests.get('http://185.46.10.111:9090/cars')
print(r.text)