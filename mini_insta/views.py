# File: views.py 
# Author: Artemios Kayas (akayas@bu.edu) 
# Description: Views page to display all my templates and holds logic to display pages
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse
from .models import Profile, Post, Photo
from .forms import CreateProfileForm, CreatePostForm

class ProfileListView(ListView):
    '''View for the show all page'''
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles'

class ProfileDetailView(DetailView):
    '''View for the profile detail page'''
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'

class CreateProfileView(CreateView):
    '''View for the create profile page'''
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_insta/create_profile.html'
    success_url = '/mini_insta/'

class PostDetailView(DetailView):
    '''View for the post detail page'''
    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'

class CreatePostView(CreateView):
    '''View for creating a new post'''
    model = Post
    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'
    
    def get_context_data(self, **kwargs):
        '''Add the profile to the context data'''
        context = super().get_context_data(**kwargs)
        # get the profile from the URL parameter
        profile_pk = self.kwargs['pk']
        profile = get_object_or_404(Profile, pk=profile_pk)
        context['profile'] = profile
        return context
    
    def form_valid(self, form):
        '''Handle form submission - attach profile and create photo'''
        # get the profile from the URL parameter
        profile_pk = self.kwargs['pk']
        profile = get_object_or_404(Profile, pk=profile_pk)

        # attach the profile to the post before saving
        form.instance.profile = profile

        # save the post
        response = super().form_valid(form)

        # OLD CODE (commented out for backwards-compatibility):
        # create a photo object if image url was provided
        # image_url = form.cleaned_data.get('image_url')
        # if image_url:
        #     Photo.objects.create(
        #         post=self.object,
        #         image_url=image_url
        #     )

        # NEW CODE: handle uploaded image files
        files = self.request.FILES.getlist('files')
        for file in files:
            Photo.objects.create(
                post=self.object,
                image_file=file
            )

        return response
    
    def get_success_url(self):
        '''Redirect to the newly created post detail page'''
        return reverse('show_post', kwargs={'pk': self.object.pk})
