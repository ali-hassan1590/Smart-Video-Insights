from django import forms

class VideoUploadForm(forms.Form):
    video = forms.FileField(label="Upload Video")
    target_language = forms.CharField(label="Target Language (Optional)", required=False)
