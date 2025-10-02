# File: models.py #
# Author: Artemios Kayas (akayas@bu.edu) #
# Description: Models page to hold all my models for the mini_insta app
from django.db import models

# Create your models here.

class Profile(models.Model): 
    '''Data structure for the profile model '''

    username = models.TextField(blank=True) 
    display_name = models.TextField(blank=True)
    profile_image_url = models.TextField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateField(auto_now=True)

    def __str__(self): 
        return f'{self.username} aka {self.display_name}'

class Post(models.Model):
    '''Data stucture for the posts'''

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateField(auto_now=True)
    caption = models.TextField(blank=True)

    def __str__(self):
        return f'{self.profile} at {self.timestamp}'

class Photo(models.Model):
    '''Data stucture for the photos'''

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.TextField(blank=True)
    timestamp = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.post} at {self.image_url}'

