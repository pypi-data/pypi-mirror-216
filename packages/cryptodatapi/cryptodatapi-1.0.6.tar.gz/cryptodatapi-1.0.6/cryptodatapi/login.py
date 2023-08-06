import requests
import os

def login(username, password): 
    headers = {
        # Already added when you pass json= but not when you pass data=
        # 'Content-Type': 'application/json',
    }
    payload = {
        'username': username, 
        'password': password
    }
    response = requests.post(url='https://cryptodatapi.com/v1/login', headers=headers, json=payload)
    statusCode = response.status_code
    bearerToken = response.json().get('Document')
    os.environ['BEARER_TOKEN'] = bearerToken    
    return {
        'statusCode': statusCode, 
        'bearerToken': bearerToken
    }