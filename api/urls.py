from django.urls import path
from .views import transcribe_video_api_view
from .views import summarize_text_api_view

urlpatterns = [
    path("transcribe/", transcribe_video_api_view, name="transcribe_video"),
    path("transcribe/summary/", summarize_text_api_view, name="summary_video")
]
