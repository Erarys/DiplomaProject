from django.urls import path
from . import views

app_name = 'speech'

urlpatterns = [
    path('content/', views.ContentView.as_view(), name='content'),
    path('record/', views.SpeechRecognition.as_view(), name='record'),
]