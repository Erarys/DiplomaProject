import io

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings

from collections import Counter

import cv2
from fer import FER
import ffmpeg
import os

from intelegence.simple import generate_answer
from voice_ai.recognize import recognize_audio
from voice_ai.speach import generate_speach


def record_page(request):
    return render(request, 'speech/speech-record.html')


@csrf_exempt
def upload_video(request):
    if request.method == 'POST':
        video_file = request.FILES.get('video')
        if video_file:
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
            file_path = os.path.join(settings.MEDIA_ROOT, video_file.name)
            # print(file_path)
            with open(file_path, 'wb+') as destination:
                for chunk in video_file.chunks():
                    destination.write(chunk)

            emotion = detect_emotion_from_video(file_path)
            audio_bytes = extract_audio_from_video(file_path)
            text = recognize_audio(audio_bytes)
            message = text + f" Эмоция говорящего: {emotion}"
            answer = generate_answer(message)
            generate_speach(answer)

            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'no file'}, status=400)

    return JsonResponse({'status': 'invalid method'}, status=405)

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



def extract_audio_from_video(video_path):
    out, _ = (
        ffmpeg.input(video_path)
        .output('pipe:', format='wav', acodec='pcm_s16le', ac=1, ar='16000')
        .run(capture_stdout=True, capture_stderr=True)
    )
    return io.BytesIO(out)

if __name__ == '__main__':
    audio = extract_audio_from_video(r'recorded_video.webm')
    print(recognize_audio(audio))