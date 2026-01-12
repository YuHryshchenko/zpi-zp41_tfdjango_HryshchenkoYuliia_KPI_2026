import tensorflow as tf
import numpy as np
import csv
from .forms import MediaForm
from django.http import HttpResponse
from django.shortcuts import render

def analyze_spectrum(request):
    classification = None
    plot_data = []

    if request.method == 'POST':
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            # Assume CSV file with single column of numbers
            file = request.FILES['media_Main_Signal']
            decoded_file = file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)
            
            # Parse data to float list
            signal = [float(row[0]) for row in reader if row]
            
            # Convert to Tensor
            signal_tensor = tf.convert_to_tensor(signal, dtype=tf.float32)
            
            # 1. Compute FFT using TensorFlow
            # Use simple Fast Fourier Transform
            fft_result = tf.signal.fft(tf.cast(signal_tensor, tf.complex64))
            magnitude = tf.abs(fft_result)
            
            # 2. Heuristic Logic: 
            # If the maximum peak in the spectrum is significantly higher than the mean, 
            # it indicates a strong periodic component (like a Sine wave).
            max_val = tf.reduce_max(magnitude)
            mean_val = tf.reduce_mean(magnitude)
            ratio = max_val / mean_val

            if ratio > 10.0:  # Threshold
                classification = "Periodic Signal (Ordered)"
            else:
                classification = "Stochastic Signal (Random Noise)"
                
            # Prepare data for simple JS chart if needed
            plot_data = magnitude.numpy()[:50].tolist() # First 50 freqs
    else:
        form = MediaForm()

    return render(request, 'signal_app/index.html', {'form': form,'classification': classification, 'plot_data': plot_data})

def success(request):
    return HttpResponse('Successfully uploaded!')