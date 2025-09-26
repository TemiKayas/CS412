# File: urls.py #
# Author: Artemios Kayas (akayas@bu.edu) #
# Description: Urls page to display all my urls for the mini_insta app
from django.urls import path
from django.conf import settings
from . import views
from .views import ProfileListView, ProfileDetailView

urlpatterns = [
    path('', ProfileListView.as_view(), name='show_all_profiles'),
    path('<int:pk>/', ProfileDetailView.as_view(), name='show_profile'),
]