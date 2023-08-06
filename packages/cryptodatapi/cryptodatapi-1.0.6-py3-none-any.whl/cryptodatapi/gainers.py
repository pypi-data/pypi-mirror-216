import requests
import json
import os

def get_gainers(id=None, sym=None):
    bearerToken = os.getenv('BEARER_TOKEN')
    url = 'https://cryptodatapi.com/v1/gainers/'
    headers = {
        'Content-Type': 'application/json', 
        'Authorization': f'Bearer {bearerToken}'
    }
    if id != None: 
        url += id
    response = requests.get(url=url, headers=headers)
    return response.json()

def put_gainers(id, payload):
    bearerToken = os.getenv('BEARER_TOKEN') 
    url = f'https://cryptodatapi.com/v1/gainers/{id}'
    headers = {
        'Content-Type': 'application/json', 
        'Authorization': f'Bearer {bearerToken}'
    }
    response = requests.put(url=url, headers=headers, data=payload)
    return response.json()

def delete_gainers(id): 
    bearerToken = os.getenv('BEARER_TOKEN')
    url = f'https://cryptodatapi.com/v1/gainers/{id}'
    headers = {
        'Content-Type': 'application/json', 
        'Authorization': f'Bearer {bearerToken}'
    }
    payload = json.dumps({
        'id': id
    })
    response = requests.delete(url=url, headers=headers, data=payload)
    return response.json()

def add_gainers(payload):
    bearerToken = os.getenv('BEARER_TOKEN')
    url = 'https://cryptodatapi.com/v1/gainers'
    headers = {
        'Content-Type': 'application/json', 
        'Authorization': f'Bearer {bearerToken}'
    }
    response = requests.post(url=url, headers=headers, data=payload)
    return response.json()