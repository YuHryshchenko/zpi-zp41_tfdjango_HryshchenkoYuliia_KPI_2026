# sound_app/views.py
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import librosa
from .forms import MediaForm
from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

# Load YAMNet model from TF Hub
yamnet_model = hub.load('https://tfhub.dev/google/yamnet/1')

def recognize_sound(request):
    top_class = None
    if request.method == 'POST':
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            audio_file = request.FILES['media_Main_Sound']
            fs = FileSystemStorage()
            filename = fs.save(audio_file.name, audio_file)
            filepath = fs.path(filename)

            # 1. Load audio at 16k sample rate (required by YAMNet)
            wav_data, _ = librosa.load(filepath, sr=16000)
            
            # 2. Run Model
            scores, embeddings, spectrogram = yamnet_model(wav_data)
            
            # 3. Process results (Average scores across all frames)
            class_scores = np.mean(scores.numpy(), axis=0)
            top_class_index = np.argmax(class_scores)
            
            # 4. Get class name (YAMNet includes a class map file usually, 
            # but for simplicity, we get the index here. In production, map index to YAMNet csv labels)
            class_map_path = yamnet_model.class_map_path().numpy().decode('utf-8')
            class_names = [x['display_name'] for x in user_friendly_class_map(class_map_path)]
            top_class = class_names[top_class_index]
    else:
        form = MediaForm()

    return render(request, 'sound_app/index.html', {'form': form, 'top_class': top_class})

def user_friendly_class_map(class_map_csv_text):
    import csv
    with open(class_map_csv_text) as csvfile:
        return list(csv.DictReader(csvfile))

def success(request):
    return HttpResponse('Successfully uploaded!')