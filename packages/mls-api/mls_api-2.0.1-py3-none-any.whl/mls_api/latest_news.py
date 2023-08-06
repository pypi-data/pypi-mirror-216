import requests
import json
import os

def get_latest_news(id=None):
    bearerToken = os.getenv('BEARER_TOKEN')
    url = 'https://mlssoccerapi.com/news/'
    headers = {
        'Content-Type': 'application/json', 
        'Authorization': f'Bearer {bearerToken}'
    }
    if id != None: 
        url += id
    response = requests.get(url=url, headers=headers)
    return response.json()

def update_latest_news(id, payload):
    bearerToken = os.getenv('BEARER_TOKEN') 
    url = f'https://mlssoccerapi.com/news/{id}'
    headers = {
        'Content-Type': 'application/json', 
        'Authorization': f'Bearer {bearerToken}'
    }
    response = requests.put(url=url, headers=headers, data=payload)
    return response.json()

def delete_latest_news(id): 
    bearerToken = os.getenv('BEARER_TOKEN')
    url = f'https://mlssoccerapi.com/news/{id}'
    headers = {
        'Content-Type': 'application/json', 
        'Authorization': f'Bearer {bearerToken}'
    }
    payload = json.dumps({
        'id': id
    })
    response = requests.delete(url=url, headers=headers, data=payload)
    return response.json()

def add_latest_news(payload):
    bearerToken = os.getenv('BEARER_TOKEN')
    url = 'https://mlssoccerapi.com/news/'
    headers = {
        'Content-Type': 'application/json', 
        'Authorization': f'Bearer {bearerToken}'
    }
    response = requests.post(url=url, headers=headers, data=payload)
    return response.json()