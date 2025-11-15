# File: views.py 
# Author: Artemios Kayas (akayas@bu.edu) 
# Description: Views page to display all my templates and holds my context dictionarys
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Joke, Picture
from .serializers import JokeSerializer, PictureSerializer
import random


def random_joke_and_picture(request):
    """Show one random joke and one random picture."""
    jokes = list(Joke.objects.all())
    pictures = list(Picture.objects.all())

    joke = random.choice(jokes) if jokes else None
    picture = random.choice(pictures) if pictures else None

    context = {
        'joke': joke,
        'picture': picture,
    }
    return render(request, 'dadjokes/random.html', context)


def all_jokes(request):
    """Show all jokes."""
    jokes = Joke.objects.all().order_by('-created_at')
    context = {'jokes': jokes}
    return render(request, 'dadjokes/jokes.html', context)


def single_joke(request, pk):
    """Show one joke by primary key."""
    joke = get_object_or_404(Joke, pk=pk)
    context = {'joke': joke}
    return render(request, 'dadjokes/joke.html', context)


def all_pictures(request):
    """Show all pictures."""
    pictures = Picture.objects.all().order_by('-created_at')
    context = {'pictures': pictures}
    return render(request, 'dadjokes/pictures.html', context)


def single_picture(request, pk):
    """Show one picture by primary key."""
    picture = get_object_or_404(Picture, pk=pk)
    context = {'picture': picture}
    return render(request, 'dadjokes/picture.html', context)


@api_view(['GET'])
def api_random_joke(request):
    """Return one random joke as JSON."""
    jokes = list(Joke.objects.all())
    if jokes:
        joke = random.choice(jokes)
        serializer = JokeSerializer(joke)
        return Response(serializer.data)
    return Response({'error': 'No jokes available'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def api_all_jokes(request):
    """Return all jokes as JSON or create a new joke."""
    if request.method == 'GET':
        jokes = Joke.objects.all()
        serializer = JokeSerializer(jokes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = JokeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def api_single_joke(request, pk):
    """Return one joke by primary key as JSON."""
    joke = get_object_or_404(Joke, pk=pk)
    serializer = JokeSerializer(joke)
    return Response(serializer.data)


@api_view(['GET'])
def api_all_pictures(request):
    """Return all pictures as JSON."""
    pictures = Picture.objects.all()
    serializer = PictureSerializer(pictures, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def api_single_picture(request, pk):
    """Return one picture by primary key as JSON."""
    picture = get_object_or_404(Picture, pk=pk)
    serializer = PictureSerializer(picture)
    return Response(serializer.data)


@api_view(['GET'])
def api_random_picture(request):
    """Return one random picture as JSON."""
    pictures = list(Picture.objects.all())
    if pictures:
        picture = random.choice(pictures)
        serializer = PictureSerializer(picture)
        return Response(serializer.data)
    return Response({'error': 'No pictures available'}, status=status.HTTP_404_NOT_FOUND)
