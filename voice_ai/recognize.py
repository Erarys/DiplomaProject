from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def recognize_audio():
    with open("voice_ai/speech.wav", "rb") as audio_file:

        client = OpenAI()
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        return transcription.text
