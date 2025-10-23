# File: models.py #
# Author: Artemios Kayas (akayas@bu.edu) #
# Description: Models page to hold all my models for the mini_insta app
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    '''Data structure for the profile model '''

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.TextField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateField(auto_now=True)


    def __str__(self):
        return f'{self.username} aka {self.display_name}'

    def get_all_posts(self):
        return Post.objects.filter(profile=self).order_by('-timestamp')

    def get_absolute_url(self):
        '''Return the URL to display this profile'''
        from django.urls import reverse
        return reverse('show_profile', kwargs={'pk': self.pk})

    def get_followers(self):
        '''Return a list of Profile objects who are following this profile'''
        follow_records = Follow.objects.filter(profile=self)
        return [follow.follower_profile for follow in follow_records]

    def get_num_followers(self):
        '''Return the count of followers'''
        return Follow.objects.filter(profile=self).count()

    def get_following(self):
        '''Return a list of Profile objects that this profile is following'''
        follow_records = Follow.objects.filter(follower_profile=self)
        return [follow.profile for follow in follow_records]

    def get_num_following(self):
        '''Return the count of profiles being followed'''
        return Follow.objects.filter(follower_profile=self).count()

    def get_post_feed(self):
        '''Return a QuerySet of Posts from profiles that this profile is following'''
        following_profiles = Follow.objects.filter(follower_profile=self).values_list('profile', flat=True)
        return Post.objects.filter(profile__in=following_profiles).order_by('-timestamp')


class Post(models.Model):
    '''Data stucture for the posts'''

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateField(auto_now=True)
    caption = models.TextField(blank=True)

    def __str__(self):
        return f'{self.profile} at {self.timestamp}'

    def get_all_photos(self):
        return Photo.objects.filter(post=self)

    def get_all_comments(self):
        '''Return all comments on this post'''
        return Comment.objects.filter(post=self).order_by('-timestamp')

    def get_likes(self):
        '''Return all likes on this post'''
        return Like.objects.filter(post=self)

class Photo(models.Model):
    '''Data stucture for the photos'''

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.TextField(blank=True)
    image_file=models.ImageField(blank=True)
    timestamp = models.DateField(auto_now=True)


    def get_image_url(self):
        if self.image_url:
            return self.image_url
        elif self.image_file:
            return self.image_file.url
        return None

    def __str__(self):
        return f'{self.post} at {self.get_image_url()}'

class Follow(models.Model):
    '''Data structure for the Follow relationship between two profiles'''

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile")
    follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="follower_profile")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.follower_profile.display_name} follows {self.profile.display_name}'

class Comment(models.Model):
    '''Data structure for comments on posts'''

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=False)

    def __str__(self):
        return f'{self.profile.display_name} on {self.post}: {self.text[:50]}'

class Like(models.Model):
    '''Data structure for likes on posts'''

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.profile.display_name} likes {self.post}'

