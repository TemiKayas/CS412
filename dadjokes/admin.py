from django.contrib import admin
from .models import Joke, Picture

# Register your models here.

@admin.register(Joke)
class JokeAdmin(admin.ModelAdmin):
    list_display = ('text', 'contributor_name', 'created_at')
    list_filter = ('created_at', 'contributor_name')
    search_fields = ('text', 'contributor_name')


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ('image_url', 'contributor_name', 'created_at')
    list_filter = ('created_at', 'contributor_name')
    search_fields = ('contributor_name',)
