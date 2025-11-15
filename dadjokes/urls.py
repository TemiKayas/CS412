# File: urls.py 
# Author: Artemios Kayas (akayas@bu.edu) 
# Description: Urls page to display all my urls for the dadjokes app
from django.urls import path
from . import views

app_name = 'dadjokes'

urlpatterns = [
    path('', views.random_joke_and_picture, name='index'),
    path('random', views.random_joke_and_picture, name='random'),
    path('jokes', views.all_jokes, name='jokes'),
    path('joke/<int:pk>', views.single_joke, name='joke'),
    path('pictures', views.all_pictures, name='pictures'),
    path('picture/<int:pk>', views.single_picture, name='picture'),

    path('api/', views.api_random_joke, name='api_random_joke'),
    path('api/random', views.api_random_joke, name='api_random_joke_alt'),
    path('api/jokes', views.api_all_jokes, name='api_all_jokes'),
    path('api/joke/<int:pk>', views.api_single_joke, name='api_single_joke'),
    path('api/pictures', views.api_all_pictures, name='api_all_pictures'),
    path('api/picture/<int:pk>', views.api_single_picture, name='api_single_picture'),
    path('api/random_picture', views.api_random_picture, name='api_random_picture'),
]
