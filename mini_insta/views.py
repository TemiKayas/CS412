from django.shortcuts import render
from django.views.generic import ListView
from .models import Profile

class ShowAllView(ListView):
    '''View for the show all page'''
    model = Profile
    template_name = 'mini_insta/show_all.html'
    context_object_name = 'profiles'
