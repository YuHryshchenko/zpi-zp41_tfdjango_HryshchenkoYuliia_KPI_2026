from django.urls import path
from . import views
from .views import analyze_video, success
from django.conf import settings
from django.conf.urls.static import static

app_name = "video_app"
urlpatterns = [
    path("", views.analyze_video, name="video"),
    path('success/', success, name='success'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)