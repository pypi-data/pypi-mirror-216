import requests
import json
import os

def get_players(id=None, offset=None, limit=None):
    bearerToken = os.getenv('BEARER_TOKEN')
    url = 'https://mlssoccerapi.com/players/'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {bearerToken}'
    }
    
    params = {}
    if offset is not None:
        params['offset'] = offset
    if limit is not None:
        params['limit'] = limit
    if id is not None:
        url += str(id)
    
    response = requests.get(url=url, headers=headers, params=params)
    return response.json()

def update_players(id, payload):
    bearerToken = os.getenv('BEARER_TOKEN') 
    url = f'https://mlssoccerapi.com/players/{id}'
    headers = {
        'Content-Type': 'application/json', 
        'Authorization': f'Bearer {bearerToken}'
    }
    response = requests.put(url=url, headers=headers, data=payload)
    return response.json()

def delete_players(id): 
    bearerToken = os.getenv('BEARER_TOKEN')
    url = f'https://mlssoccerapi.com/players/{id}'
    headers = {
        'Content-Type': 'application/json', 
        'Authorization': f'Bearer {bearerToken}'
    }
    payload = json.dumps({
        'id': id
    })
    response = requests.delete(url=url, headers=headers, data=payload)
    return response.json()

def add_players(payload):
    bearerToken = os.getenv('BEARER_TOKEN')
    url = 'https://mlssoccerapi.com/players/'
    headers = {
        'Content-Type': 'application/json', 
        'Authorization': f'Bearer {bearerToken}'
    }
    response = requests.post(url=url, headers=headers, data=payload)
    return response.json()