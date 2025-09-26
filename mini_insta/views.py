# File: views.py #}
# Author: Artemios Kayas (akayas@bu.edu) #
# Description: Views page to display all my templates and holds logic to display pages
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile

class ProfileListView(ListView):
    '''View for the show all page'''
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles'

class ProfileDetailView(DetailView):
    '''View for the profile detail page'''
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'