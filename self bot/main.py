from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import StreamingResponse
import io
import stt
import tts
import gpt

app = FastAPI(title="Full Voice Chat Bot")

@app.post("/chat/audio")
async def full_voice_chat(audio: UploadFile):
    try:
        # 1. STT: Ovozdan text olish
        audio_bytes = await audio.read()
        user_text = stt.speech_to_text(audio_bytes)

        # 2. AI modelga yuborish
        reply_text = gpt.ask_gpt(user_text)

        # 3. TTS: Javobni ovozga aylantirish
        audio_reply = tts.text_to_speech(reply_text)

        # 4. Ovozli va text javoblarni qaytarish
        return {
            "user_text": user_text,
            "reply_text": reply_text,
            "audio_base64": io.BytesIO(audio_reply).getvalue().hex()  # yoki base64 encode qilsa ham bo‘ladi
        }
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
