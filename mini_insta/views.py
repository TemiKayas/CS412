# File: views.py #}
# Author: Artemios Kayas (akayas@bu.edu) #
# Description: Views page to display all my templates and holds logic to display pages
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile
from .forms import CreateProfileForm

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

class CreateProfileView(CreateView):
    '''View for the create profile page'''
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_insta/create_profile.html'
    success_url = '/mini_insta/'
