from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings
from .models import *
from .forms import ContestantForm, ContactUsForm, UserFeedBackForm

def base_view(request):
    socia_media_links = SocialMedialinks.objects.first()

    return render(request, 'main/base.html', {'social_media_links': socia_media_links})

def home(request):
    current_year = datetime.now().year
    next_year = current_year + 1
    contestants = Contestant.objects.filter(approved=True)
    header_image = HeaderImage.objects.filter().first()
    performances = Performance.objects.all()
    artists = InvitedArtist.objects.filter(created_at__year = current_year)
    registration_status = RegistrationStatus.objects.first()

    if registration_status:
        registration_open = registration_status.is_registration_open
    else:
        registration_open = False

    context = {
        'performances': performances,
        'artists': artists,
        'contestants': contestants,
        'next_year': next_year,
        'registration_open': registration_open,
        'header_image': header_image,
    }
    return render(request, 'main/index.html', context)


def about(request):
    about_info = About.objects.first()
    return render(request, 'main/about.html', {'about_info': about_info})

def mission(request):
    mission_info = Mission.objects.first()
    return render(request, 'main/mission.html', {'mission_info': mission_info})

def contact(request):
    contact_update = ContactPage.objects.first()
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = ContactUsForm()

    return render(request, 'main/contact.html', {'contact_update': contact_update, 'form': form})

def blog(request):
    posts = Post.objects.all()
    return render(request, 'main/blog.html', {'posts': posts})

def blog_details(request, pk):
    post = get_object_or_404(Post, id=pk)

    if request.method == 'POST':
        form = UserFeedBackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.post = post
            feedback.save()
            return redirect('main:blog_detail', pk=pk)
    else:
        form = UserFeedBackForm()

    return render(request, 'main/blog_detail.html', {'form': form, 'post': post})


class BlogDetailView(DetailView):
    model = Post
    template_name = 'main/post_detail.html'
    context_object_name = 'blog'


def media_list(request):
    media_items = UploadVideo.objects.all()
    return render(request, 'main/media.html', {'media_items': media_items})

# Contestant registration Form
def create_contestant(request):
    # Check if registration is open
    registration_status = RegistrationStatus.objects.first()

    if registration_status and hasattr(registration_status, 'is_registration_open'):
        registration_open = registration_status.is_registration_open
    else:
        registration_open = False  # Set a default value when registration_status or is_registration_open is None

    if not registration_open:
        return render(request, 'main/registration_closed.html')

    if request.method == 'POST':
        form = ContestantForm(request.POST, request.FILES)
        if form.is_valid():
            contestant_instance = form.save()
            send_admin_email(contestant_instance)
            return redirect('thank_you')
    else:
        form = ContestantForm()

    return render(request, 'main/contestant.html', {'form': form})

def send_admin_email(contestant_instance):
    subject = 'New Contestant Registration'
    message = f'A new contestant has registered.\n\nName: {contestant_instance.full_name}\nPhone Number: {contestant_instance.phone_number}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ['missdnk@gmail.com']
    send_mail(subject, message, from_email, recipient_list)

def send_contestant_approval_email(contestant_instance):
    subject = 'Your Contestant Registration is Approved'
    message = f'Dear {contestant_instance.full_name},\n\nCongratulations! Your registration has been approved.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient = [contestant_instance.email]
    send_mail(subject, message, from_email, recipient)

def song_list(request):
    songs = Song.objects.all()
    return render(request, 'main/song_list.html', {'songs': songs})

def song_detail(request, pk):
    song = get_object_or_404(Song, pk=pk)
    return render(request, 'main/song_detail.html', {'song': song})

# def download_song(request, pk):
#     song = get_object_or_404(Song, pk=pk)
#     response = FileResponse(song.audio_file)
#     return response