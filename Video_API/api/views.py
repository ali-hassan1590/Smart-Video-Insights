from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import VideoTranscriptionSerializer
from django.core.files.storage import default_storage
from moviepy.editor import VideoFileClip
import os
import whisper

# ✅ Load Whisper model once globally
whisper_model = whisper.load_model("base")


class TranscribeVideoView(APIView):
    def post(self, request):
        serializer = VideoTranscriptionSerializer(data=request.data)
        
        if serializer.is_valid():
            video_file = serializer.validated_data['video']
            target_lang = serializer.validated_data.get('target_language', None)

            # ✅ Save uploaded video to media/videos/
            video_path = default_storage.save(f"videos/{video_file.name}", video_file)
            audio_path = video_path.rsplit('.', 1)[0] + '.mp3'

            try:
                # ✅ Extract audio from video using moviepy
                clip = VideoFileClip(default_storage.path(video_path))
                clip.audio.write_audiofile(default_storage.path(audio_path), verbose=False, logger=None)
                
                # ✅ Transcribe audio using Whisper
                result = whisper_model.transcribe(default_storage.path(audio_path))
                
                response_data = {
                    "original_language": result["language"],
                    "transcription": result["text"]
                }

                # 🔁 Optional: Handle translation (not implemented yet)
                if target_lang:
                    response_data["translated_to"] = target_lang
                    response_data["translation"] = f"(Translation logic for {target_lang} goes here.)"

                return Response(response_data, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
