from urllib import response
from flask import request
import requests

BASE = 'http://127.0.0.1:5000'

data = {
    "username": 'neko3',
    'password': "789",
    'email': 'neko3@gmail.com'
}

#response = requests.post(BASE + "/register", json=data)
#response = requests.get(BASE + "/login", json={'username': 'neko', 'password': '123'})
#response = requests.get(BASE +"/verifyemail", json={'email': 'neko1@gmail.com'})
response = requests.get(BASE + '/login/product/quantity')
print(response)