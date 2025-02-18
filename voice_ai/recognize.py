from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def recognize_audio(wav_buffer):
    client = OpenAI()
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=wav_buffer
    )
    return transcription.text
