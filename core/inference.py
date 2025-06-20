import requests

class Inference:
    def __init__(self, base_url="http://localhost:11434/api/generate", model_name="llama3"):
        self.base_url = base_url
        self.model_name = model_name

    def generate_answer(self, prompt):
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False  # stream True bo'lsa ketma ket output bo'ladi
        }
        response = requests.post(self.base_url, json=payload)
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "")
        else:
            return "Modeldan javob olishda xatolik yuz berdi."
