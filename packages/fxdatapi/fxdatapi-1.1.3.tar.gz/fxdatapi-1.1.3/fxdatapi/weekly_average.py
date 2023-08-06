import requests
import json

class WeeklyAverage:
    def __init__(self, headers):
        self.base_url = 'https://fxdatapi.com/v1'
        self.headers = headers

    def get_weekly_average(self, start_date, end_date):
        url = f'{self.base_url}/weekly_average/{start_date}/{end_date}'
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get weekly average: {response.text}")
