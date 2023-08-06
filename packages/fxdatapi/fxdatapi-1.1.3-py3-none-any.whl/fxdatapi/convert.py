import requests
import json

class Convert:
    def __init__(self, headers):
        self.base_url = 'https://fxdatapi.com/v1'
        self.headers = headers

    def convert_currency(self, username, date, base_currency, target_currency, amount):
        url = f'{self.base_url}/convert'
        data = {
            'username': username,
            'date': date,
            'base_currency': base_currency,
            'target_currency': target_currency,
            'amount': amount
        }
        response = requests.post(url, headers=self.headers, data=json.dumps(data))
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to convert currency: {response.text}")
