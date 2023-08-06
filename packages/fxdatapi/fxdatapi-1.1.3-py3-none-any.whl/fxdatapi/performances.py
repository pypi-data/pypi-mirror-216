import requests
import json

class Performances:
    def __init__(self, headers):
        self.base_url = 'https://fxdatapi.com/v1'
        self.headers = headers

    def get_performances(self, username):
        url = f'{self.base_url}/performances'
        params = {
            'username': username
        }
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get performances: {response.text}")

    def get_performance(self, uuid, username):
        url = f'{self.base_url}/performances/{uuid}'
        params = {
            'username': username
        }
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get performance: {response.text}")
