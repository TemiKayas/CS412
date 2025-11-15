# File: models.py 
# Author: Artemios Kayas (akayas@bu.edu) 
# Description: Models page to display all my models for the dadjokes app
from django.db import models



class Joke(models.Model):
    """Model to store dad jokes."""
    text = models.TextField()
    contributor_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text[:50]}... by {self.contributor_name}"


class Picture(models.Model):
    """Model to store silly images/GIFs."""
    image_url = models.URLField(max_length=500)
    contributor_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Picture by {self.contributor_name}"
