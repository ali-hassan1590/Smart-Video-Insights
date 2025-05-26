from django.urls import path
from .views import TranscribeVideoView

urlpatterns = [
    path('transcribe-video/', TranscribeVideoView.as_view(), name='transcribe-video'),
]
