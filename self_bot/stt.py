import requests
from io import BytesIO
from auth_token import token_manager

def speech_to_text(audio_bytes: bytes) -> str:
    token = token_manager.get_token()
    url = "https://speech.tuit.uz/recog/"
    headers = {"Authorization": f"JWT {token}"}

    file_like = BytesIO(audio_bytes)
    file_like.seek(0)

    files = {
        'audio': ('audio.wav', file_like, 'audio/wav')
    }

    response = requests.post(url, headers=headers, files=files)
    response.raise_for_status()  # agar 500 yoki 400 chiqsa xato ko‘rsatadi

    # JSON emas, oddiy matn
    return response.text.strip()
