import requests
import time

class TokenManager:
    def __init__(self):
        self.token = None
        self.expiry = 0  # timestamp

    def get_token(self):
        if self.token is None or time.time() > self.expiry:
            print("🔄 Getting new token...")
            url = "https://speech.tuit.uz/token/"
            data = {"username": "user", "password": "XLj7RbZT2cTJm6n"}
            response = requests.post(url, data=data)
            response.raise_for_status()
            json_data = response.json()
            self.token = json_data["access"]
            self.expiry = time.time() + 540  # 9 minut ishlatamiz xavfsizlik uchun
        return self.token

token_manager = TokenManager()
