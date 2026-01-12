# creative_app/views.py
from django.shortcuts import render
from .ai_model import mood_ai
from .forms import CommentForm
from django.http import HttpResponse

def generate_atmosphere(request):
    color_hex = "#ffffff"
    text_input = ""
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            text_input = form.cleaned_data['description']
            if text_input:
                r, g, b = mood_ai.predict_color(text_input)
                # Convert to Hex
                color_hex = '#{:02x}{:02x}{:02x}'.format(r, g, b)
    else:
        form = CommentForm()
            
    return render(request, 'creative_app/index.html', {'form': form, 'color': color_hex, 'text': text_input})

def success(request):
    return HttpResponse('Successfully uploaded!')
