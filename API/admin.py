from django.contrib import admin

# Register your models here.

from API.models import UserProfile, Hackeathon, UserComment, UserPost

class Profile(admin.ModelAdmin):
    list_display = ('id', 'user', 'bio', 'githublink', 'linkedinlink', 'twitterlink', 'instagramlink', 'facebooklink')
admin.site.register(UserProfile, Profile)

class HackeathonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'start_date', 'end_date', 'registration_start_date', 'registration_end_date', 'registration_fee', 'prize')
admin.site.register(Hackeathon, HackeathonAdmin)

class UserCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'content', 'created_at')
admin.site.register(UserComment, UserCommentAdmin)

class UserPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'content', 'created_at')
admin.site.register(UserPost, UserPostAdmin)
