# from django.shortcuts import render
# from django.core.files.storage import default_storage
# from moviepy import VideoFileClip
# import whisper
# import os
# from .forms import VideoUploadForm

# whisper_model = whisper.load_model("base")

# LANGUAGE_CHOICES = {
#     "af": "Afrikaans", "am": "Amharic", "ar": "Arabic", "az": "Azerbaijani", "be": "Belarusian", 
#     "bg": "Bulgarian", "bn": "Bengali", "bs": "Bosnian", "ca": "Catalan", "cs": "Czech", "cy": "Welsh", 
#     "da": "Danish", "de": "German", "el": "Greek", "en": "English", "es": "Spanish", "et": "Estonian", 
#     "fa": "Persian", "fi": "Finnish", "fr": "French", "gl": "Galician", "gu": "Gujarati", "he": "Hebrew", 
#     "hi": "Hindi", "hr": "Croatian", "ht": "Haitian Creole", "hu": "Hungarian", "hy": "Armenian", 
#     "id": "Indonesian", "is": "Icelandic", "it": "Italian", "ja": "Japanese", "jw": "Javanese", 
#     "ka": "Georgian", "kk": "Kazakh", "km": "Khmer", "kn": "Kannada", "ko": "Korean", "la": "Latin", 
#     "lt": "Lithuanian", "lv": "Latvian", "mg": "Malagasy", "mk": "Macedonian", "ml": "Malayalam", 
#     "mn": "Mongolian", "mr": "Marathi", "ms": "Malay", "my": "Burmese", "ne": "Nepali", "nl": "Dutch", 
#     "no": "Norwegian", "pa": "Punjabi", "pl": "Polish", "pt": "Portuguese", "ro": "Romanian", 
#     "ru": "Russian", "sa": "Sanskrit", "sd": "Sindhi", "si": "Sinhala", "sk": "Slovak", "sl": "Slovenian", 
#     "so": "Somali", "sq": "Albanian", "sr": "Serbian", "su": "Sundanese", "sv": "Swedish", "sw": "Swahili", 
#     "ta": "Tamil", "te": "Telugu", "tg": "Tajik", "th": "Thai", "tk": "Turkmen", "tl": "Tagalog", 
#     "tr": "Turkish", "uk": "Ukrainian", "ur": "Urdu", "uz": "Uzbek", "vi": "Vietnamese", "xh": "Xhosa", 
#     "yi": "Yiddish", "yo": "Yoruba", "zh": "Chinese", "zu": "Zulu"
# }


# def transcribe_video_template_view(request):
#     result = None
#     error = None

#     if request.method == "POST":
#         form = VideoUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             video_file = form.cleaned_data['video']
#             target_lang = form.cleaned_data.get('target_language')

#             try:
#                 video_path = default_storage.save(f"videos/{video_file.name}", video_file)
#                 audio_path = video_path.rsplit('.', 1)[0] + '.mp3'

#                 clip = VideoFileClip(default_storage.path(video_path))
#                 clip.audio.write_audiofile(default_storage.path(audio_path), logger=None)

#                 result_data = whisper_model.transcribe(default_storage.path(audio_path))

#                 result = {
#                     "original_language": result_data["language"],
#                     "transcription": result_data["text"]
#                 }

#                 if target_lang:
#                     result["translated_to"] = target_lang
#                     result["translation"] = f"(Translation logic for {target_lang} goes here.)"

#             except Exception as e:
#                 error = str(e)
#         else:
#             error = "Invalid form data"
#     else:
#         form = VideoUploadForm()

#     return render(request, "video_upload.html", {
#         "form": form,
#         "result": result,
#         "error": error,
#         "language_choices": LANGUAGE_CHOICES
#     })

# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse
# from django.core.files.storage import default_storage
# from moviepy import VideoFileClip
# import whisper
# import torch
# import os
# from .forms import VideoUploadForm

# device = "cuda" if torch.cuda.is_available() else "cpu"
# print(f"Using device: {device}")
# whisper_model = whisper.load_model("base", device=device)

# LANGUAGE_CHOICES = {
#     "af": "Afrikaans", "am": "Amharic", "ar": "Arabic", "az": "Azerbaijani", "be": "Belarusian", 
#     "bg": "Bulgarian", "bn": "Bengali", "bs": "Bosnian", "ca": "Catalan", "cs": "Czech", "cy": "Welsh", 
#     "da": "Danish", "de": "German", "el": "Greek", "en": "English", "es": "Spanish", "et": "Estonian", 
#     "fa": "Persian", "fi": "Finnish", "fr": "French", "gl": "Galician", "gu": "Gujarati", "he": "Hebrew", 
#     "hi": "Hindi", "hr": "Croatian", "ht": "Haitian Creole", "hu": "Hungarian", "hy": "Armenian", 
#     "id": "Indonesian", "is": "Icelandic", "it": "Italian", "ja": "Japanese", "jw": "Javanese", 
#     "ka": "Georgian", "kk": "Kazakh", "km": "Khmer", "kn": "Kannada", "ko": "Korean", "la": "Latin", 
#     "lt": "Lithuanian", "lv": "Latvian", "mg": "Malagasy", "mk": "Macedonian", "ml": "Malayalam", 
#     "mn": "Mongolian", "mr": "Marathi", "ms": "Malay", "my": "Burmese", "ne": "Nepali", "nl": "Dutch", 
#     "no": "Norwegian", "pa": "Punjabi", "pl": "Polish", "pt": "Portuguese", "ro": "Romanian", 
#     "ru": "Russian", "sa": "Sanskrit", "sd": "Sindhi", "si": "Sinhala", "sk": "Slovak", "sl": "Slovenian", 
#     "so": "Somali", "sq": "Albanian", "sr": "Serbian", "su": "Sundanese", "sv": "Swedish", "sw": "Swahili", 
#     "ta": "Tamil", "te": "Telugu", "tg": "Tajik", "th": "Thai", "tk": "Turkmen", "tl": "Tagalog", 
#     "tr": "Turkish", "uk": "Ukrainian", "ur": "Urdu", "uz": "Uzbek", "vi": "Vietnamese", "xh": "Xhosa", 
#     "yi": "Yiddish", "yo": "Yoruba", "zh": "Chinese", "zu": "Zulu"
# }

# @csrf_exempt
# def transcribe_video_api_view(request):
#     if request.method != "POST":
#         return JsonResponse({"error": "Only POST method is allowed."}, status=405)

#     form = VideoUploadForm(request.POST, request.FILES)
#     if not form.is_valid():
#         return JsonResponse({"error": "Invalid form data.", "details": form.errors}, status=400)

#     video_file = form.cleaned_data['video']
#     target_lang = form.cleaned_data.get('target_language')

#     try:
#         video_path = default_storage.save(f"videos/{video_file.name}", video_file)
#         audio_path = video_path.rsplit('.', 1)[0] + '.mp3'

#         try:
#             clip = VideoFileClip(default_storage.path(video_path))
#             clip.audio.write_audiofile(default_storage.path(audio_path), logger=None)
#         except FileNotFoundError as ffmpeg_error:
#             return JsonResponse({
#                 "error": "FFmpeg not found. Please install FFmpeg and add it to your system PATH.",
#                 "details": str(ffmpeg_error)
#             }, status=500)

#         if target_lang and target_lang in LANGUAGE_CHOICES:
#             result_data = whisper_model.transcribe(default_storage.path(audio_path), language=target_lang)
#         else:
#             result_data = whisper_model.transcribe(default_storage.path(audio_path))

#         result = {
#             "language_used": target_lang if target_lang else result_data["language"],
#             "transcription": result_data["text"]
#         }
#         return JsonResponse({"result": result}, status=200)

#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)









# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse
# from django.core.files.storage import default_storage
# from moviepy import VideoFileClip
# import whisper
# import torch
# import os
# from .forms import VideoUploadForm

# device = "cuda" if torch.cuda.is_available() else "cpu"
# print(f"Using device: {device}")
# whisper_model = whisper.load_model("base", device=device)



# summarizer_device = 0 if torch.cuda.is_available() else -1
# summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=summarizer_device)




# @csrf_exempt
# def transcribe_video_api_view(request):
#     if request.method != "POST":
#         return JsonResponse({"error": "Only POST method is allowed."}, status=405)

#     form = VideoUploadForm(request.POST, request.FILES)
#     if not form.is_valid():
#         return JsonResponse({"error": "Invalid form data.", "details": form.errors}, status=400)

#     video_file = form.cleaned_data['video']

#     try:
#         video_path = default_storage.save(f"videos/{video_file.name}", video_file)
#         audio_path = video_path.rsplit('.', 1)[0] + '.mp3'

#         try:
#             clip = VideoFileClip(default_storage.path(video_path))
#             clip.audio.write_audiofile(default_storage.path(audio_path), logger=None)
#         except FileNotFoundError as ffmpeg_error:
#             return JsonResponse({
#                 "error": "FFmpeg not found. Please install FFmpeg and add it to your system PATH.",
#                 "details": str(ffmpeg_error)
#             }, status=500)

#         # Check if audio file exists and is not empty
#         audio_full_path = default_storage.path(audio_path)
#         if not os.path.exists(audio_full_path):
#             return JsonResponse({"error": "Audio extraction failed: audio file not found."}, status=500)
#         if os.path.getsize(audio_full_path) == 0:
#             return JsonResponse({"error": "Audio extraction failed: audio file is empty."}, status=500)

#         # Now transcribe
#         result_data = whisper_model.transcribe(audio_full_path)

#         result = {
#             "language_used": result_data["language"],
#             "transcription": result_data["text"]
#         }
#         return JsonResponse({"result": result}, status=200)

#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)
    

# @csrf_exempt
# def summarize_text_api_view(request):
#     if request.method != "POST":
#         return JsonResponse({"error": "Only POST method is allowed."}, status=405)

#     try:
#         data = json.loads(request.body)
#         text = data.get("text", "").strip()
#         if not text:
#             return JsonResponse({"error": "No text provided for summarization."}, status=400)

#         summary = summarizer(text, max_length=200, min_length=60, do_sample=False)
#         summary_text = summary[0]['summary_text']

#         return JsonResponse({"summary": summary_text}, status=200)
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)







from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.storage import default_storage
from moviepy import VideoFileClip
import whisper
import torch
import os
import json
from transformers import pipeline
from .forms import VideoUploadForm

from keybert import KeyBERT
import spacy

# Device setup
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")
whisper_model = whisper.load_model("base", device=device)

summarizer_device = 0 if torch.cuda.is_available() else -1
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=summarizer_device)


@csrf_exempt
def transcribe_video_api_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method is allowed."}, status=405)

    form = VideoUploadForm(request.POST, request.FILES)
    if not form.is_valid():
        return JsonResponse({"error": "Invalid form data.", "details": form.errors}, status=400)

    video_file = form.cleaned_data['video']

    try:
        video_path = default_storage.save(f"videos/{video_file.name}", video_file)
        audio_path = video_path.rsplit('.', 1)[0] + '.mp3'

        try:
            clip = VideoFileClip(default_storage.path(video_path))
            clip.audio.write_audiofile(default_storage.path(audio_path), logger=None)
        except FileNotFoundError as ffmpeg_error:
            return JsonResponse({
                "error": "FFmpeg not found. Please install FFmpeg and add it to your system PATH.",
                "details": str(ffmpeg_error)
            }, status=500)

        audio_full_path = default_storage.path(audio_path)
        if not os.path.exists(audio_full_path):
            return JsonResponse({"error": "Audio extraction failed: audio file not found."}, status=500)
        if os.path.getsize(audio_full_path) == 0:
            return JsonResponse({"error": "Audio extraction failed: audio file is empty."}, status=500)

        result_data = whisper_model.transcribe(audio_full_path)

        result = {
            "language_used": result_data["language"],
            "transcription": result_data["text"]
        }
        return JsonResponse({"result": result}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def summarize_text_api_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method is allowed."}, status=405)

    try:
        if not request.body:
            return JsonResponse({"error": "Empty request body."}, status=400)

        data = json.loads(request.body.decode("utf-8"))
        text = data.get("text", "").strip()

        if not text:
            return JsonResponse({"error": "No text provided for summarization."}, status=400)

        summary = summarizer(text, max_length=200, min_length=60, do_sample=False)
        summary_text = summary[0]['summary_text']
        return JsonResponse({"summary": summary_text}, status=200)

    except json.JSONDecodeError as e:
        return JsonResponse({"error": "Invalid JSON", "details": str(e)}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def generate_tags_title_api_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method is allowed."}, status=405)

    try:
        if not request.body:
            return JsonResponse({"error": "Empty request body."}, status=400)

        data = json.loads(request.body.decode("utf-8"))
        text = data.get("text", "").strip()

        if not text:
            return JsonResponse({"error": "No text provided for tag/title generation."}, status=400)

        # Keyword tags using KeyBERT
        kw_model = KeyBERT()
        keywords = kw_model.extract_keywords(text, top_n=5)
        keyword_tags = [kw[0] for kw in keywords]

        # Named entities using spaCy
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        entity_tags = list(set([ent.text for ent in doc.ents]))

        # Title generation using summarizer
        title_summary = summarizer(text, max_length=30, min_length=5, do_sample=False)
        title = title_summary[0]['summary_text']

        return JsonResponse({
            "tags": {
                "keywords": keyword_tags,
                "entities": entity_tags
            },
            "generated_title": title
        }, status=200)

    except json.JSONDecodeError as e:
        return JsonResponse({"error": "Invalid JSON", "details": str(e)}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
