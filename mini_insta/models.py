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