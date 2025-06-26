import openai
import os
from dotenv import load_dotenv
from rag_engine import RAGEngine

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

rag = RAGEngine()

def ask_gpt(user_input: str) -> str:
    chunks = rag.retrieve(user_input)
    context = "\n---\n".join(chunks)

    system_prompt = (
        f"Faqat quyidagi bilim asosida javob bering:\n{context}\n\n"
        f"Agar javob  topishda qiynalsangiz yoki topa olmasangiz  yuklangan malumotlar embedding ga mos ravishda toliq va aniq javob bering userni toliq va aniq contextli javoblaringiz orqali qoniqtiring "
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
