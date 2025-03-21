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

# def recognize_audio():
#     with open("recorded_video.webm", "rb") as audio_file:
#
#         client = OpenAI()
#         transcription = client.audio.transcriptions.create(
#             model="whisper-1",
#             file=audio_file
#         )
#         return transcription.text
if __name__ == "__main__":
    recognize_audio()
    #<class '_io.BufferedReader'>
    # <_io.BufferedReader name='speech.wav'>

    # <_io.BytesIO object at 0x000001FF2C5A3B50>
    # <class '_io.BytesIO'>