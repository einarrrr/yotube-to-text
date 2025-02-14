from fastapi import FastAPI
import yt_dlp
import whisper
import os

app = FastAPI()
model = whisper.load_model("base")

def descargar_audio(url):
    opciones = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio.mp3',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}]
    }
    with yt_dlp.YoutubeDL(opciones) as ydl:
        ydl.download([url])

@app.post("/transcribir/")
def transcribir(video_url: str):
    descargar_audio(video_url)
    result = model.transcribe("audio.mp3")
    os.remove("audio.mp3")
    return {"texto": result["text"]}

# Para ejecutar el backend
# uvicorn main:app --reload
