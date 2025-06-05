from django.urls import path
from .views import transcribe_video_template_view

urlpatterns = [
    path("transcribe/", transcribe_video_template_view, name="transcribe_video"),
]
