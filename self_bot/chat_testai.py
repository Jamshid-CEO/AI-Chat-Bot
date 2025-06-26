from fastapi import FastAPI
from pydantic import BaseModel
import openai

app = FastAPI()

openai.api_key = "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"

class ChatRequest(BaseModel):
    user_message: str

@app.post("/chat")
async def chat(req: ChatRequest):
    response = openai.ChatCompletion.create(
        model="gpt-4o",  # yoki boshqa model nomi
        messages=[
            {"role": "system", "content": "Siz foydalanuvchiga yordam beruvchi assistentsiz."},
            {"role": "user", "content": req.user_message}
        ],
        max_tokens=500
    )
    reply = response['choices'][0]['message']['content']
    return {"reply": reply}
