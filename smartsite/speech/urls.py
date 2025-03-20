from django.urls import path
from . import views

app_name = 'speech'

urlpatterns = [
    path('', views.record_page, name='record'),
    path('upload-photo/', views.upload_video, name='upload_video'),
]