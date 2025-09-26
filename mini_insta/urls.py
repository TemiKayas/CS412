from django.urls import path
from django.conf import settings
from . import views
from .views import show_all_profiles

urlpatterns = [
    path('', show_all_profiles.as_view(), name='show_all_profiles'),
]