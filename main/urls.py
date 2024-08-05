from django.urls import path
from .views import *

app_name = 'main'

urlpatterns = [
    path('base/', base_view, name='base'),
    path('home/', home, name='home'),
    path('about/', about, name='about'),
    path('mission/', mission, name='mission'),
    path('contact/', contact, name='contact'),
    path('blog/', blog, name='blog'),
    path('blog_detail/<int:pk>/', blog_details, name='blog_detail'),
    path('media/', media_list, name='media'),
    path('contestant/', create_contestant, name='contestant'),
    path('song_list/', song_list, name='song_list'),
    path('song/<int:pk>/', song_detail, name='song_detail'),
    path('<int:pk>/', BlogDetailView.as_view(), name='blog-detail'),
]
