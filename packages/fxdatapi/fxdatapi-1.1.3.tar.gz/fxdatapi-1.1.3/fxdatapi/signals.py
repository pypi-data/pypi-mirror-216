import requests
import json

class Signals:
    def __init__(self, headers):
        self.base_url = 'https://fxdatapi.com/v1'
        self.headers = headers

    def get_signals(self, username):
        url = f'{self.base_url}/signals'
        params = {
            'username': username
        }
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get signals: {response.text}")

    def get_signal(self, uuid, username):
        url = f'{self.base_url}/signals/{uuid}'
        params = {
            'username': username
        }
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get signal: {response.text}")
