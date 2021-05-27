import requests
import json
from requests.auth import HTTPBasicAuth


# BE TOKENS


# gauti bands readonly

# r = requests.get('http://127.0.0.1:8000/bands')
# posts = (json.loads(r.text))
# print(posts)


# registruoti naują vartotoją

# data = {'username': 'demo5', 'password': 'demo5demo5'}
# r = requests.post('http://127.0.0.1:8000/signup', data=data)
# print(r.text)


# Įrašyti naują grupę
# Be prisijungimo:

# data = {'name': 'Massive Attack'}
# r = requests.post("http://127.0.0.1:8000/bands", data=data)
# print(r.text)

# Su prisijungimu:

# data = {'name': 'Alva Noto'}
# r = requests.post("http://127.0.0.1:8000/bands", auth=HTTPBasicAuth('demo5', 'demo5demo5'), data=data)
# print(r.text)


# SU TOKENS

# Gauname žetoną:

# data = {'username': 'demo5', 'password': 'demo5demo5'}
#
# r = requests.post("http://127.0.0.1:8000/api-token-auth/", data=data)
# print(r.text)

my_token = '70fa39ec0c8b854f8e331e5fdb4452f2d67b5b03'

# Įrašyti naują grupę ( su token)

# data = {'name': 'Alva Noto'}
# headers = {'Authorization': f'Token {my_token}'}
# r = requests.post("http://127.0.0.1:8000/bands", data=data, headers=headers)
# print(r.text)

# Gauti grupes ( su token)

headers = {'Authorization': f'Token {my_token}'}
r = requests.get("http://127.0.0.1:8000/bands", headers=headers)
print(r.text)