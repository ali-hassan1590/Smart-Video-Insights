from rest_framework import serializers

class VideoTranscriptionSerializer(serializers.Serializer):
    video = serializers.FileField()
    target_language = serializers.CharField(required=False)
