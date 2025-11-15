# File: urls.py
# Author: Artemios Kayas (akayas@bu.edu)
# Description: URLs for the voter_analytics app
from django.urls import path
from .views import VoterListView, VoterDetailView

urlpatterns = [
    path('', VoterListView.as_view(), name='voters'),
    path('voter/<int:pk>', VoterDetailView.as_view(), name='voter'),
]
