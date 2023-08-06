import requests
import json
import os

def get_fixtures(id=None):
    bearerToken = os.getenv('BEARER_TOKEN')
    url = 'https://mlssoccerapi.com/fixtures/'
    headers = {
        'Content-Type': 'application/json', 
        'Authorization': f'Bearer {bearerToken}'
    }
    if id != None: 
        url += id
    response = requests.get(url=url, headers=headers)
    return response.json()

def update_fixtures(id, payload):
    bearerToken = os.getenv('BEARER_TOKEN') 
    url = f'https://mlssoccerapi.com/fixtures/{id}'
    headers = {
        'Content-Type': 'application/json', 
        'Authorization': f'Bearer {bearerToken}'
    }
    response = requests.put(url=url, headers=headers, data=payload)
    return response.json()

def delete_fixtures(id): 
    bearerToken = os.getenv('BEARER_TOKEN')
    url = f'https://mlssoccerapi.com/fixtures/{id}'
    headers = {
        'Content-Type': 'application/json', 
        'Authorization': f'Bearer {bearerToken}'
    }
    payload = json.dumps({
        'id': id
    })
    response = requests.delete(url=url, headers=headers, data=payload)
    return response.json()

def add_fixtures(payload):
    bearerToken = os.getenv('BEARER_TOKEN')
    url = 'https://mlssoccerapi.com/fixtures/'
    headers = {
        'Content-Type': 'application/json', 
        'Authorization': f'Bearer {bearerToken}'
    }
    response = requests.post(url=url, headers=headers, data=payload)
    return response.json()