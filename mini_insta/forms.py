# File: forms.py #
# Author: Artemios Kayas (akayas@bu.edu) #
# Description: Forms page to hold all my forms for the mini_insta app
from django import forms
from .models import *

class CreateProfileForm(forms.ModelForm):
    '''Form for the profile model'''

    class Meta:
        '''Meta class for the profile form'''
        model = Profile
        fields = ['display_name', 'username', 'profile_image_url', 'bio_text']

class CreatePostForm(forms.ModelForm):
    '''Form for the post model'''

    class Meta:
        '''Meta class for the post form'''
        model = Post
        fields = ['caption']  