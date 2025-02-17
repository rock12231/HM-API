from django.contrib import admin

# Register your models here.

from API.models import ProfileModel, CommentModel, PostModel, HackeathonModel, ForgotPasswordModel

class Profile(admin.ModelAdmin):
    list_display = ('id', 'user', 'bio','gender')
admin.site.register(ProfileModel, Profile)

class HackeathonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'start_date', 'end_date', 'registration_start_date', 'registration_end_date', 'registration_fee', 'prize')
admin.site.register(HackeathonModel, HackeathonAdmin)

class UserCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'created_at', 'updated_at', 'content')
admin.site.register(CommentModel, UserCommentAdmin)

class UserPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'created_at', 'updated_at', 'member', 'types', 'deleted', 'content')
admin.site.register(PostModel, UserPostAdmin)

class UserForgotPasswordAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'otp', 'created_at', 'updated_at')
admin.site.register(ForgotPasswordModel, UserForgotPasswordAdmin)   
