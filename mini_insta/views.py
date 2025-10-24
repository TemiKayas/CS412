# File: views.py
# Author: Artemios Kayas (akayas@bu.edu)
# Description: Views page to display all my templates and holds logic to display pages
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse
from django.db import models
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile, Post, Photo
from .forms import CreateProfileForm, CreatePostForm, UpdateProfileForm

class ProfileLoginRequiredMixin(LoginRequiredMixin):
    '''Custom mixin that requires login and provides helper to get logged-in user's Profile'''

    def get_login_url(self):
        '''Return the URL to the login page'''
        return reverse('login')

    def get_profile(self):
        '''Return the Profile associated with the logged-in user
        Note: Uses .first() to handle cases where multiple Profiles
        are associated with the same User (e.g., from migration defaults)'''
        profile = Profile.objects.filter(user=self.request.user).first()
        if not profile:
            # If no profile found, raise 404
            from django.http import Http404
            raise Http404("No Profile found for this user")
        return profile

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

class CreatePostView(ProfileLoginRequiredMixin, CreateView):
    '''View for creating a new post'''
    model = Post
    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'

    def get_context_data(self, **kwargs):
        '''Add the profile to the context data'''
        context = super().get_context_data(**kwargs)
        # get the profile of the logged-in user
        context['profile'] = self.get_profile()
        return context

    def form_valid(self, form):
        '''Handle form submission - attach profile and create photo'''
        # get the profile of the logged-in user
        profile = self.get_profile()

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

class UpdateProfileView(ProfileLoginRequiredMixin, UpdateView):
    '''View for updating a profile'''
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'

    def get_object(self):
        '''Return the Profile of the logged-in user'''
        return self.get_profile()

    def get_success_url(self):
        '''Redirect to the profile page after successful update'''
        return reverse('show_profile', kwargs={'pk': self.object.pk})

class DeletePostView(LoginRequiredMixin, DeleteView):
    '''View for deleting a post'''
    model = Post
    template_name = 'mini_insta/delete_post_form.html'

    def get_context_data(self, **kwargs):
        '''Add post and profile to context'''
        context = super().get_context_data(**kwargs)
        context['post'] = self.object
        context['profile'] = self.object.profile
        return context

    def get_success_url(self):
        '''Redirect to profile page after successful delete'''
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

class UpdatePostView(LoginRequiredMixin, UpdateView):
    '''View for updating a post'''
    model = Post
    fields = ['caption']
    template_name = 'mini_insta/update_post_form.html'

    def get_context_data(self, **kwargs):
        '''Add post to context'''
        context = super().get_context_data(**kwargs)
        context['post'] = self.object
        return context

    def get_success_url(self):
        '''Redirect to post page after successful update'''
        return reverse('show_post', kwargs={'pk': self.object.pk})

class ShowFollowersDetailView(DetailView):
    '''View for showing followers of a profile'''
    model = Profile
    template_name = 'mini_insta/show_followers.html'
    context_object_name = 'profile'

class ShowFollowingDetailView(DetailView):
    '''View for showing profiles that a profile is following'''
    model = Profile
    template_name = 'mini_insta/show_following.html'
    context_object_name = 'profile'

class PostFeedListView(ProfileLoginRequiredMixin, ListView):
    '''View for showing the post feed for a profile'''
    model = Post
    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'posts'

    def get_queryset(self):
        '''Return the posts for the profiles being followed'''
        profile = self.get_profile()
        return profile.get_post_feed()

    def get_context_data(self, **kwargs):
        '''Add the profile to the context data'''
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_profile()
        return context

class SearchView(ProfileLoginRequiredMixin, ListView):
    '''View for searching profiles and posts'''
    template_name = 'mini_insta/search_results.html'
    context_object_name = 'posts'

    def dispatch(self, request, *args, **kwargs):
        '''Handle the request and determine which template to show'''
        if 'query' not in self.request.GET:
            profile = self.get_profile()
            return render(request, 'mini_insta/search.html', {'profile': profile})
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        '''Return posts that match the search query'''
        query = self.request.GET.get('query', '')
        return Post.objects.filter(caption__icontains=query)

    def get_context_data(self, **kwargs):
        '''Add profile, query, and matching profiles to context'''
        context = super().get_context_data(**kwargs)
        profile = self.get_profile()
        query = self.request.GET.get('query', '')

        context['profile'] = profile
        context['query'] = query
        context['posts'] = self.get_queryset()
        context['profiles'] = Profile.objects.filter(
            models.Q(username__icontains=query) |
            models.Q(display_name__icontains=query) |
            models.Q(bio_text__icontains=query)
        )
        return context

class LogoutConfirmationView(TemplateView):
    '''View for the logout confirmation page'''
    template_name = 'mini_insta/logged_out.html'

class MyProfileView(ProfileLoginRequiredMixin, DetailView):
    '''Redirect to the logged-in user's profile'''
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'

    def get_object(self):
        '''Return the Profile of the logged-in user'''
        return self.get_profile()
