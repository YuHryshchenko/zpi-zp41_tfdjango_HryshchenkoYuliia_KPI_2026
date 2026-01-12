from django.urls import path
from . import views
from .views import generate_atmosphere, success
from django.conf import settings
from django.conf.urls.static import static

app_name = "creative_app"
urlpatterns = [
    path("", views.generate_atmosphere, name="creative"),
    path('success/', success, name='success'),
]
