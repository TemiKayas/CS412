# File: serializers.py 
# Author: Artemios Kayas (akayas@bu.edu) 
# Description: Serializers page to display all my serializers for the dadjokes app
from rest_framework import serializers
from .models import Joke, Picture


class JokeSerializer(serializers.ModelSerializer):
    """Serializer for Joke model."""
    class Meta:
        model = Joke
        fields = ['id', 'text', 'contributor_name', 'created_at']


class PictureSerializer(serializers.ModelSerializer):
    """Serializer for Picture model."""
    class Meta:
        model = Picture
        fields = ['id', 'image_url', 'contributor_name', 'created_at']
