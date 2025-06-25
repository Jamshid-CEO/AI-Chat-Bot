import openai
import os
from dotenv import load_dotenv
from rag_engine import RAGEngine

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

rag = RAGEngine()

def ask_gpt(user_input: str) -> str:
    context = "\n".join(rag.retrieve(user_input, top_k=3))

    system_prompt = (
        f"Faqat quyidagi bilim asosida javob bering:\n{context}\n\n"
        f"Agar javob topilmasa, 'Kechirasiz, bu mavzu bo‘yicha ma'lumot yo‘q.' deb yozing."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input},
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.3
    )
    return response['choices'][0]['message']['content']
