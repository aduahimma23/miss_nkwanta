from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.dispatch import receiver
from django.db import models
from django.utils import *
from django.core.exceptions import ValidationError

def validate_year(value):
    if value < 1900 or value > 2100:
        raise ValidationError(f"{value} is not a valid year.")

class SocialMedialinks(models.Model):
    facebook = models.URLField(unique=True, blank=False)
    instagram = models.URLField(unique=True, blank=False)
    whatsapp = models.URLField(unique=True, blank=False)
    tiktok = models.URLField(unique=True, blank=False)


class About(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=5000, blank=False)

    def __str__(self):
        return self.title
    
    
class Mission(models.Model):
    title = models.CharField(max_length=100)
    mission_content = models.TextField(max_length=5000, blank=False)

    def __str__(self):
        return self.title
    

class HeaderImage(models.Model):
    POSITION_CHOICES = [
        ('First', 'First'),
        ('First Runners up', 'First Runners up'),
        ('Second Runners Up', 'Second Runners Up'),
    ]
    
    name = models.CharField(max_length=100, blank=False)
    year = models.IntegerField(default=2024, validators=[validate_year])
    position = models.CharField(max_length=20, choices=POSITION_CHOICES, default='First')
    image = models.ImageField(upload_to='header_images/', null=True, blank=True)

    def __str__(self):
        return f'{self.name}: {self.year} - {self.position}'

class UploadVideo(models.Model):
    title = models.CharField(max_length=50,null=False, default='Trending Videos')
    description = models.TextField(blank=True)
    video_title = models.FileField(upload_to='videos/', default='Trending Videos')
    upload_time = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.title
    
    @property
    def short_upload_time(self):
        return self.upload_time.strftime('%b %d, %Y %H:%M')


class NewsCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name
    

class Post(models.Model):
    category = models.ManyToManyField(NewsCategory)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    title = models.CharField(max_length=150)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-details', args=[str(self.id)])
    

class UserFeedBack(models.Model):
    post = models.OneToOneField('Post', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    feedback = models.TextField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.send_notification()

    def send_notification(self):
        try:
            subject ='New User FeedBack Submission'
            message = f'A new feedback has been submitted:\n\nNmae: {self.mame}\nEmail: {self.email}\nFeedback: {self.feedback}'
        except Exception as e:
            print(f"Error sending notification: {e}")

    def __str__(self):
        return f'Feedback for {self.post.title} \n By {self.name}'

class RegistrationStatus(models.Model):
    is_registration_open = models.BooleanField(default=False)

    def __str__(self):
        return f"Registration is {'Open' if self.is_registration_open else 'Closed'}"

class Contestant(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    full_name = models.CharField(max_length=150)
    stage_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    phone_number = models.IntegerField(blank=False, default=2335834637)
    email = models.EmailField(default='missdnk@gmail.com')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Female')
    image = models.ImageField(upload_to='media', null=False, unique=True, blank=False)
    town = models.CharField(max_length=150)
    occupation = models.CharField(max_length=150)
    role_model = models.CharField(max_length=50)
    hobby = models.CharField(max_length=255)
    favourite_food = models.CharField(max_length=150)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_year = models.IntegerField(default=timezone.now().year)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.age > 40:
            raise ValidationError("Contestants must be 35 years or younger to register.")
    
        if self.gender in ['Male', 'Other']:
                raise ValidationError("Male's are not allowed to register for this contest.")

    def __str__(self):
        return self.full_name
    
class Pageant(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    date = models.DateField()
    location = models.CharField(max_length=255)
    contestants = models.ManyToManyField(Contestant)

    def __str__(self):
        return f"{self.id}: {self.name}"
    

class ContactUs(models.Model):
    full_name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(blank=False)
    message = models.TextField(max_length=500, blank=False)

    def __str__(self):
        return self.full_name
    
class ContactPage(models.Model):
    email = models.EmailField()
    location = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    facebook_url = models.URLField(blank=True, null=True)
    twitter_handle = models.CharField(max_length=50, blank=True, null=True)
    instagram_handle = models.CharField(max_length=50, blank=True, null=True)
    tiktok_handle = models.CharField(max_length=50, blank=True, null=True)
    youtube_channel = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return "Contact Page"


class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    audio_file = models.FileField(upload_to='audio_files/')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class InvitedArtist(models.Model):
    name = models.CharField(max_length=150, blank=False, unique=True)
    image = models.ImageField(upload_to='invited_artist')
    short_content = models.CharField(max_length=255, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'Name {self.name}'

class Performance(models.Model):
    year = models.DateField(auto_now=True)
    video_url = models.FileField(upload_to='performance_videos')
    content = models.CharField(max_length=255, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
