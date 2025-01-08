import requests
from dotenv import load_dotenv
load_dotenv()
import os

class ProductApi:
    def __init__(self, session_cookies, base_url=os.getenv("HOST")):
        self.base_url = base_url
        self.session = requests.Session()
        for name, value in session_cookies.items():
            self.session.cookies.set(name, value)
    
    def send_request(self, endpoint, method='GET', data=None):
        url = f'{self.base_url}/{endpoint}'
        response = self.session.request(method, url, json=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def getPendingProductsCount(self, params: dict):
        response = self.session.post(f'{self.base_url}/new_api/public/products/pending/count', params=params)
        response.raise_for_status()
        return response.json()

# Ejemplo de uso:
# api_client = APIClient(base_url='https://api.example.com', session_cookies=session_cookies)