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
    
    image_url = forms.CharField(
        required=False,
        label='Image URL',
        help_text='Enter the URL of an image for this post',
        widget=forms.TextInput(attrs={'placeholder': 'https://example.com/image.jpg'})
    )

    class Meta:
        '''Meta class for the post form'''
        model = Post
        fields = ['caption']  