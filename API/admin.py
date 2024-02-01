from django.contrib import admin

# Register your models here.

from API.models import UserProfile

class Profile(admin.ModelAdmin):
    list_display = ('id', 'user', 'bio', 'githublink', 'linkedinlink', 'twitterlink', 'instagramlink', 'facebooklink')
admin.site.register(UserProfile, Profile)