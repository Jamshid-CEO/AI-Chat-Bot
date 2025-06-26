from fastapi import FastAPI, UploadFile, Form, File
import os, shutil, base64
from dotenv import load_dotenv
from self_bot import stt, tts, gpt
from self_bot.rag_engine import RAGEngine
from self_bot.db import SessionLocal
from self_bot.models import ChatHistory

app = FastAPI(title="Full Voice Chat Bot with RAG")
load_dotenv()

UPLOAD_FOLDER = os.getenv('KNOWLEDGE_BASE_DIR')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

rag = RAGEngine()

def save_chat(user_text: str, reply_text: str):
    db = SessionLocal()
    history = ChatHistory(user_text=user_text, reply_text=reply_text)
    db.add(history)
    db.commit()
    db.close()

@app.post("/upload")
async def file_upload(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    rag.add_document(file_path)

    return {
        "message": f"✅ Fayl '{file.filename}' yuklandi va bazaga qo‘shildi",
        "file_path": file_path
    }

@app.post("/chat/text")
async def chat_from_text(text: str = Form(...)):
    reply_text = gpt.ask_gpt(text)
    save_chat(text, reply_text)
    audio_bytes = tts.text_to_speech(reply_text)
    audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

    return {
        "user_text": text,
        "reply_text": reply_text,
        "audio_base64": audio_base64
    }

@app.post("/chat/audio")
async def chat_from_audio(audio: UploadFile):
    audio_bytes = await audio.read()
    user_text = stt.speech_to_text(audio_bytes)
    reply_text = gpt.ask_gpt(user_text)
    save_chat(user_text, reply_text)
    audio_reply = tts.text_to_speech(reply_text)
    audio_base64 = base64.b64encode(audio_reply).decode("utf-8")

    return {
        "user_text": user_text,
        "reply_text": reply_text,
        "audio_base64": audio_base64
    }
