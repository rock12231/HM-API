from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    college = models.CharField(max_length=100, blank=True)
    branch = models.CharField(max_length=20, blank=True)
    year = models.CharField(max_length=10, blank=True)
    batch = models.CharField(max_length=10, blank=True)
    student = models.BooleanField(default=True)
    professional = models.BooleanField(default=False)
    # avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    githublink = models.TextField(blank=True)
    linkedinlink = models.TextField(blank=True)
    twitterlink = models.TextField(blank=True)
    instagramlink = models.TextField(blank=True)
    facebooklink = models.TextField(blank=True)
    stackoverflowlink = models.TextField(blank=True)
    otherlink = models.TextField(blank=True)
    # location = models.CharField(max_length=30, blank=True)
