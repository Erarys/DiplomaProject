from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()



def recognize_audio(audio_bytes):
    audio_bytes.seek(0)
    audio_bytes.name = "speech.wav"
    client = OpenAI()
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_bytes
    )
    return transcription.text
