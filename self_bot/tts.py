import requests
from self_bot.auth_tokens import token_manager

def text_to_speech(text: str) -> bytes:
    token = token_manager.get_token()
    url = "https://speech.tuit.uz/synt/"
    headers = {"Authorization": f"JWT {token}"}
    data = {
        "text": text,
        "version": "1"
    }

    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.content
