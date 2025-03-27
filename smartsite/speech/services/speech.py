# from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
# import pygame
# import time
import os

from smartsite import settings

load_dotenv()


def generate_speach(message: str) -> None:
    client = OpenAI()
    speech_file_path = os.path.join(settings.MEDIA_ROOT, "speech_answer.wav")
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=message,
    )
    response.stream_to_file(speech_file_path)

    return speech_file_path

    # Инициализируем pygame и воспроизводим аудио
    # pygame.mixer.init()
    # pygame.mixer.music.load(speech_file_path)
    # pygame.mixer.music.play()
    #
    # while pygame.mixer.music.get_busy():
    #     time.sleep(1)

    # pygame.mixer.quit()

