from django.urls import path
from . import views
from .views import recognize_sound, success
from django.conf import settings
from django.conf.urls.static import static

app_name = "sound_app"
urlpatterns = [
    path("", views.recognize_sound, name="sound"),
    path('success/', success, name='success'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)