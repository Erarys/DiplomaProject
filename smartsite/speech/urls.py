from django.urls import path
from . import views

app_name = 'speech'

urlpatterns = [
    path('', views.SpeechRecognition.as_view(), name='record'),
]