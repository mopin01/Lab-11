from django.shortcuts import render, redirect, get_object_or_404
from .models import Video
from .forms import VideoForm, SearchForm
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models.functions import Lower

# Home page view
def home(request):
    app_name = 'Random Videos'
    return render(request, 'video_collection/home.html', {'app_name': app_name})

def add(request):
    if request.method == 'POST':
        # Create video form
        new_video_form = VideoForm(request.POST)
        # Check if form data is valid
        if new_video_form.is_valid():
            try:
                # Save video and redirect to video list page
                new_video_form.save()
                return redirect('video_list')
            # Catch validation and integrity errors
            except ValidationError:
                messages.warning(request, 'Invalid YouTube URL')
            except IntegrityError:
                messages.warning(request, 'You already added that video')
        # Dislpay error if invalid
        messages.warning(request, 'Please check the data entered')
        return render(request, 'video_collection/add.html', {'new_video_form': new_video_form})

    new_video_form = VideoForm()
    return render(request, 'video_collection/add.html', {'new_video_form': new_video_form})

def video_list(request):
    # Create search form
    search_form = SearchForm(request.GET)

    # Check if form data is valid
    if search_form.is_valid():
        # Search videos and order by name
        search_term = search_form.cleaned_data['search_term']
        videos = Video.objects.filter(name__icontains=search_term).order_by(Lower('name'))
    else:
        # Create new search form and order all videos by name
        search_form = SearchForm()
        videos = Video.objects.order_by(Lower('name'))

    return render(request, 'video_collection/video_list.html', {'videos': videos, 'search_form': search_form})

# Render video details page
def video_details(request, video_pk):
    video = get_object_or_404(Video, pk=video_pk)
    return render(request, 'video_collection/video_details.html', {'video': video})