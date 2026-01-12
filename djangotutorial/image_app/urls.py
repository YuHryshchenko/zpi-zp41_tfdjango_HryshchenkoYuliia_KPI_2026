from django.urls import path
from .views import classify_image, success
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = "image_app"
urlpatterns = [
    path("", views.classify_image, name="image"),
    path('success/', success, name='success'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)