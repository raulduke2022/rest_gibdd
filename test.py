import requests


r = requests.get('http://localhost:8080/time')
print(r.text)
