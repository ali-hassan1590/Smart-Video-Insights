from django.shortcuts import render
from django.core.files.storage import default_storage
from moviepy import VideoFileClip
import whisper
import os
from .forms import VideoUploadForm

whisper_model = whisper.load_model("base")

LANGUAGE_CHOICES = {
    "af": "Afrikaans", "am": "Amharic", "ar": "Arabic", "az": "Azerbaijani", "be": "Belarusian", 
    "bg": "Bulgarian", "bn": "Bengali", "bs": "Bosnian", "ca": "Catalan", "cs": "Czech", "cy": "Welsh", 
    "da": "Danish", "de": "German", "el": "Greek", "en": "English", "es": "Spanish", "et": "Estonian", 
    "fa": "Persian", "fi": "Finnish", "fr": "French", "gl": "Galician", "gu": "Gujarati", "he": "Hebrew", 
    "hi": "Hindi", "hr": "Croatian", "ht": "Haitian Creole", "hu": "Hungarian", "hy": "Armenian", 
    "id": "Indonesian", "is": "Icelandic", "it": "Italian", "ja": "Japanese", "jw": "Javanese", 
    "ka": "Georgian", "kk": "Kazakh", "km": "Khmer", "kn": "Kannada", "ko": "Korean", "la": "Latin", 
    "lt": "Lithuanian", "lv": "Latvian", "mg": "Malagasy", "mk": "Macedonian", "ml": "Malayalam", 
    "mn": "Mongolian", "mr": "Marathi", "ms": "Malay", "my": "Burmese", "ne": "Nepali", "nl": "Dutch", 
    "no": "Norwegian", "pa": "Punjabi", "pl": "Polish", "pt": "Portuguese", "ro": "Romanian", 
    "ru": "Russian", "sa": "Sanskrit", "sd": "Sindhi", "si": "Sinhala", "sk": "Slovak", "sl": "Slovenian", 
    "so": "Somali", "sq": "Albanian", "sr": "Serbian", "su": "Sundanese", "sv": "Swedish", "sw": "Swahili", 
    "ta": "Tamil", "te": "Telugu", "tg": "Tajik", "th": "Thai", "tk": "Turkmen", "tl": "Tagalog", 
    "tr": "Turkish", "uk": "Ukrainian", "ur": "Urdu", "uz": "Uzbek", "vi": "Vietnamese", "xh": "Xhosa", 
    "yi": "Yiddish", "yo": "Yoruba", "zh": "Chinese", "zu": "Zulu"
}


def transcribe_video_template_view(request):
    result = None
    error = None

    if request.method == "POST":
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video_file = form.cleaned_data['video']
            target_lang = form.cleaned_data.get('target_language')

            try:
                video_path = default_storage.save(f"videos/{video_file.name}", video_file)
                audio_path = video_path.rsplit('.', 1)[0] + '.mp3'

                clip = VideoFileClip(default_storage.path(video_path))
                clip.audio.write_audiofile(default_storage.path(audio_path), logger=None)

                result_data = whisper_model.transcribe(default_storage.path(audio_path))

                result = {
                    "original_language": result_data["language"],
                    "transcription": result_data["text"]
                }

                if target_lang:
                    result["translated_to"] = target_lang
                    result["translation"] = f"(Translation logic for {target_lang} goes here.)"

            except Exception as e:
                error = str(e)
        else:
            error = "Invalid form data"
    else:
        form = VideoUploadForm()

    return render(request, "video_upload.html", {
        "form": form,
        "result": result,
        "error": error,
        "language_choices": LANGUAGE_CHOICES
    })
