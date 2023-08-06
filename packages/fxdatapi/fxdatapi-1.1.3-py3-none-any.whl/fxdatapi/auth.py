import requests
import json

class Auth:
    def __init__(self):
        self.base_url = 'https://fxdatapi.com/v1'
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

    def login(self, username, password):
        url = f'{self.base_url}/login'
        data = {
            'username': username,
            'password': password
        }
        response = requests.post(url, headers=self.headers, data=json.dumps(data))
        
        if response.status_code == 200:
            user_type = response.cookies.get('user_type')
            username_cookie = response.cookies.get('username')
            self.headers.update({
                'Cookie': f'user_type={user_type}; username={username_cookie}'
            })
            return response.json()
        else:
            raise Exception(f"Login failed: {response.text}")