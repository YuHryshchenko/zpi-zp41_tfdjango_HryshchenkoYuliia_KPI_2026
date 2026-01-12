from django.db import models

class Comment(models.Model):
    description = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
