from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.conf import settings

import os
import json
from speech.services.intelegence import generate_answer
from speech.services.speech_recognition import recognize_audio
from speech.services.speech import generate_speach
from speech.services.emotion_recognition import detect_emotion_from_video
from speech.services.separate_video_audio import extract_audio_from_video
from speech.services.voice_emotion import voice_emotion_recognition


class SpeechRecognition(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.emotion = "Не передано"
        self.voice_emotion = "Не передано"

    def get(self, request):
        return render(request, 'speech/speech-record.html')

    def post(self, request):

        if request.method == 'POST':
            video_file = request.FILES.get('video')
            process_mode_str = request.POST.get('process_mode')
            process_mode = json.loads(process_mode_str)

            if video_file:
                os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
                file_path = os.path.join(settings.MEDIA_ROOT, video_file.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in video_file.chunks():
                        destination.write(chunk)

                if process_mode["is_face_emotion"]:
                    self.emotion = detect_emotion_from_video(file_path)

                audio_bytes = extract_audio_from_video(file_path)
                text = recognize_audio(audio_bytes)
                if process_mode["is_voice_emotion"]:
                    self.voice_emotion = voice_emotion_recognition(audio_bytes)

                message = text + f" Эмоция лица: {self.emotion}, Эмоций голоса {self.voice_emotion}"
                print(message)

                answer = generate_answer(message, self.emotion, self.voice_emotion)
                audio_file_path = generate_speach(answer)
                audio_url = request.build_absolute_uri(settings.MEDIA_URL + os.path.basename(audio_file_path))
                return JsonResponse({'audio_url': audio_url})

            return JsonResponse({'status': 'no file'}, status=400)

        return JsonResponse({'status': 'invalid method'}, status=405)
