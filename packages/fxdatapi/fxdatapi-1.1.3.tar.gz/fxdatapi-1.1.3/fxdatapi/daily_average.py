import requests
import json

class DailyAverage:
    def __init__(self, headers):
        self.base_url = 'https://fxdatapi.com/v1'
        self.headers = headers

    def get_daily_average(self, date):
        url = f'{self.base_url}/daily_average/{date}'
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get daily average: {response.text}")
