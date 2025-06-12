from django.urls import path
from .views import (
    transcribe_video_api_view,
    summarize_text_api_view,
    generate_tags_title_api_view
)

urlpatterns = [
    path("transcribe/", transcribe_video_api_view, name="transcribe_video"),
    path("transcribe/summary/", summarize_text_api_view, name="summary_video"),
    path("transcribe/tags-title/", generate_tags_title_api_view, name="tags_title_video"),
]
