import requests
import json

class MarginsSpreads:
    def __init__(self, headers):
        self.base_url = 'https://fxdatapi.com/v1'
        self.headers = headers

    def get_margins_spreads(self, username, day, month, year):
        url = f'{self.base_url}/margins_spreads'
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
            raise Exception(f"Failed to get margins and spreads: {response.text}")

    def get_margins_spreads_currency(self, uuid, username, day, month, year):
        url = f'{self.base_url}/margins_spreads/{uuid}'
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
            raise Exception(f"Failed to get margins and spreads for currency: {response.text}")
