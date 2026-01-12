from django import forms
from .models import Media

class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['media_Main_Video']