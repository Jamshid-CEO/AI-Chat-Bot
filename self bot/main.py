from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import StreamingResponse
import io
import base64
import stt
import tts
import gpt

app = FastAPI(title="Full Voice Chat Bot")

@app.post("/chat/audio")
async def speech_to_text_endpoint(audio: UploadFile):
    try:
        audio_bytes = await audio.read()
        text = stt.speech_to_text(audio_bytes)
        return {"text": text}
    except Exception as e:
        return {"error": str(e)}

# Agar faqat TTS test qilmoqchi bo'lsangiz:
@app.post("/chat/text")
async def text_to_speech(text: str = Form(...)):
    try:
        audio_bytes = tts.text_to_speech(text)
        return StreamingResponse(io.BytesIO(audio_bytes), media_type="audio/wav")
    except Exception as e:
        return {"error": str(e)}
