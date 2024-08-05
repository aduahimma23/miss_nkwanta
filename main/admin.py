from django.contrib import admin
from django.urls import reverse, path
from django.utils.safestring import mark_safe
from .models import *


admin.site.register(RegistrationStatus)
admin.site.register(NewsCategory)
admin.site.register(ContactPage)
admin.site.register(About)
admin.site.register(Mission)
admin.site.register(Performance)
admin.site.register(SocialMedialinks)


class ContestantAdmin(admin.ModelAdmin):
    list_display = ['image', 'full_name', 'stage_name', 'approved']
    list_filter = ['approved', 'gender']
    search_fields = ['full_name', 'stage_name', 'town', 'occupation']

    actions = ['approve_selected_contestants']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('approve_selected_contestants/', self.admin_site.admin_view(self.approve_selected_contestants),
                 name='contestant_approve_selected_contestants'),
        ]
        return custom_urls + urls


    def approve_selected_contestants(self, request, queryset):
        queryset.update(approved=True)

    approve_selected_contestants.short_description = 'Approve selected contestants'

admin.site.register(Contestant, ContestantAdmin)


class MediaModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'video_title')
    search_fields = ['title', 'description']

admin.site.register(UploadVideo, MediaModelAdmin)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'content')

    def get_absolute_url(self, obj):
        return reverse('post_detail', args=[str(obj.id)])
    

class HeaderImageAdmin(admin.ModelAdmin):
    list_display = ('position', 'year')

    def display_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')
    
    display_image.short_description = 'Image Preview'

admin.site.register(HeaderImage, HeaderImageAdmin)


@admin.register(UserFeedBack)
class UserFeedBackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'feedback')


class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'upload_date')
    search_fields = ('title', 'artist')
    list_filter = ('artist', 'upload_date')

admin.site.register(Song, SongAdmin)