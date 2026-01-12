from django.db import models

class Media(models.Model):
    media_Main_Img = models.ImageField(upload_to='media/')

    def __str__(self):
        return self.name