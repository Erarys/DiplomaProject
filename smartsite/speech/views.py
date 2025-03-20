from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import os
from django.conf import settings

def record_page(request):
    return render(request, 'speech/speech-record.html')


@csrf_exempt
def upload_video(request):
    if request.method == 'POST':
        video_file = request.FILES.get('video')
        if video_file:
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
            file_path = os.path.join(settings.MEDIA_ROOT, video_file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in video_file.chunks():
                    destination.write(chunk)
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'no file'}, status=400)
    return JsonResponse({'status': 'invalid method'}, status=405)
