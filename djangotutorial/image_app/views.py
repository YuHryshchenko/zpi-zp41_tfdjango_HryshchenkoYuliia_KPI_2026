import numpy as np
from django.shortcuts import render
from django.http import HttpResponse
from .forms import MediaForm
from .models import Media
from django.core.files.storage import FileSystemStorage
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image as keras_image

# Load model globally to keep it in memory
model = MobileNetV2(weights='imagenet')

def classify_image(request):
    prediction = None
    prediction_percent = None
    if request.method == 'POST':
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            # Save file temporarily
            image_file = request.FILES['media_Main_Img']
            fs = FileSystemStorage()
            filename = fs.save(image_file.name, image_file)
            file_path = fs.path(filename)

            # Preprocess for MobileNetV2
            img = keras_image.load_img(file_path, target_size=(224, 224))
            img_array = keras_image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)

            # Predict
            preds = model.predict(img_array)
            # Get top 3 predictions: [(class, description, prob), ...]
            prediction = decode_predictions(preds, top=3)[0]
            prediction_percent = [
                (id, label, prob * 100)
                for (id, label, prob) in prediction
            ]
               
    else:
        form = MediaForm()

    return render(request, 'image_app/index.html', {'form': form, 'prediction': prediction_percent})

def success(request):
    return HttpResponse('Successfully uploaded!')