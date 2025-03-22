import os
from collections import Counter

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '1'  # Включает oneDNN

import cv2
from fer import FER


def record_face_emotion(stop_event, result_queue):
    emotions = []
    # Загружаем видео с камеры
    cap = cv2.VideoCapture(0)
    detector = FER()

    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            break

        # Распознаем эмоции
        result = detector.detect_emotions(frame)

        if result:
            emotion = max(result[0]['emotions'], key=result[0]['emotions'].get)
            emotions.append(emotion)
            print("Эмоция:", emotion)

    cap.release()
    cv2.destroyAllWindows()

    emotions = Counter(emotions)
    avg_emotion = emotions.most_common(1)[0][0]
    result_queue.put(avg_emotion)


def detect_emotion_from_video(video_path):
    emotions = []
    cap = cv2.VideoCapture(video_path)
    detector = FER()

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        result = detector.detect_emotions(frame)
        if result:
            emotion = max(result[0]['emotions'], key=result[0]['emotions'].get)
            emotions.append(emotion)

    cap.release()
    emotions = Counter(emotions)
    if emotions:
        return emotions.most_common(1)[0][0]
    return 'neutral'