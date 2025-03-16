from intelegence.simple import generate_answer
from voice_ai.audio_rec import record_audio
from voice_ai.recognize import recognize_audio
from voice_ai.speach import generate_speach

from face_emotion_rec.face_emotion import record_face_emotion

import time
import multiprocessing


def run_flow(stop_event, result_queue):
    record_audio()
    stop_event.set()  # Сигнализируем о завершении работы


if __name__ == '__main__':
    stop_event = multiprocessing.Event()  # Событие для управления остановкой func2
    result_queue = multiprocessing.Queue()
    process_1 = multiprocessing.Process(target=run_flow, args=(stop_event, result_queue))
    process_2 = multiprocessing.Process(target=record_face_emotion, args=(stop_event, result_queue))

    process_1.start()
    process_2.start()

    process_1.join()  # Ждем завершения func1
    process_2.join()  # Ждем завершения func2

    while not result_queue.empty():
        result = result_queue.get()


    message = recognize_audio()
    print("User:", message)
    message = message + f" Эмоция говорящего: {result}"
    answer = generate_answer(message)
    print("AI:", answer)
    generate_speach(answer)
