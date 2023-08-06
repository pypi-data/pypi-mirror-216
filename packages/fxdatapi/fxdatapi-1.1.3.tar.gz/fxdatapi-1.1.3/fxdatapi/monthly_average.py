import requests
import json

class MonthlyAverage:
    def __init__(self, headers):
        self.base_url = 'https://fxdatapi.com/v1'
        self.headers = headers

    def get_monthly_average(self, year, month):
        url = f'{self.base_url}/monthly_average/{year}/{month}'
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get monthly average: {response.text}")
