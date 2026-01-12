# video_app/views.py
import cv2
import numpy as np
import os
from django.shortcuts import render
from .forms import MediaForm
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions

# Reusing the same model architecture is fine
video_model = MobileNetV2(weights='imagenet')

def analyze_video(request):
    result = None
    if request.method == 'POST':
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            video_file = request.FILES['media_Main_Video']
            fs = FileSystemStorage()
            filename = fs.save(video_file.name, video_file)
            video_path = fs.path(filename)

            # 1. Capture the video
            cap = cv2.VideoCapture(video_path)
            
            # 2. Get total frames and jump to the middle
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames // 2)
            
            # 3. Read the frame
            ret, frame = cap.read()
            cap.release()

            if ret:
                # 4. Convert BGR (OpenCV) to RGB (TensorFlow)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_resized = cv2.resize(frame_rgb, (224, 224))
                
                # 5. Predict
                img_array = np.expand_dims(frame_resized, axis=0)
                img_array = preprocess_input(img_array.astype(np.float32))
                preds = video_model.predict(img_array)
                result = decode_predictions(preds, top=1)[0][0][1] # Just get the class name
    else:
        form = MediaForm()

    return render(request, 'video_app/index.html', {'form': form, 'result': result})

def success(request):
    return HttpResponse('Successfully uploaded!')