from django.db import models
from django.core.validators import FileExtensionValidator

class Media(models.Model):
    # The 'upload_to' argument specifies a subdirectory within MEDIA_ROOT
    media_Main_Sound = models.FileField(upload_to='media/', null=True, verbose_name="", 
                                 validators=[FileExtensionValidator(allowed_extensions=['wav','mp3'])])
    
    def __str__(self):
        return self.name
