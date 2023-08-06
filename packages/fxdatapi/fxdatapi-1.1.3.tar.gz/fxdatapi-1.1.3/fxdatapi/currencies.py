import requests
import json

class Currencies:
    def __init__(self, headers):
        self.base_url = 'https://fxdatapi.com/v1'
        self.headers = headers

    def get_currencies(self, username, day, month, year):
        url = f'{self.base_url}/currencies'
        params = {
            'username': username,
            'day': day,
            'month': month,
            'year': year
        }
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get currencies: {response.text}")

    def get_currency(self, uuid, username, day, month, year):
        url = f'{self.base_url}/currencies/{uuid}'
        params = {
            'username': username,
            'day': day,
            'month': month,
            'year': year
        }
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get currency: {response.text}")