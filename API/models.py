from django.db import models
from django.contrib.auth.models import User


GENDER_CHOICES = [ ('M', 'Male'), ('F', 'Female'), ('O', 'Other'),]
OCCUPATION_CHOICES = [ ('S', 'Student'), ('P', 'Professional'),]
TYPE_CHOICES = [ ('Member', 'Member'), ('Team', 'Team'),]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    college = models.CharField(max_length=100, blank=True)
    branch = models.CharField(max_length=20, blank=True)
    year = models.CharField(max_length=10, blank=True)
    batch = models.CharField(max_length=10, blank=True)
    occupation = models.CharField(max_length=1, choices=OCCUPATION_CHOICES, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    githublink = models.TextField(blank=True)
    linkedinlink = models.TextField(blank=True)
    twitterlink = models.TextField(blank=True)
    instagramlink = models.TextField(blank=True)
    facebooklink = models.TextField(blank=True)
    stackoverflowlink = models.TextField(blank=True)
    otherlink = models.TextField(blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)


class UserComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('UserPost', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='comment_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='comment_dislikes', blank=True)


class UserPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hackeathon = models.TextField(blank=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    member = models.IntegerField()
    types = models.CharField(max_length=10, choices=TYPE_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='post_dislikes', blank=True)
    comments = models.ManyToManyField(UserComment, related_name='post_comments', blank=True)
    intrested = models.ManyToManyField(User, related_name='post_intrested', blank=True)
    deleted = models.BooleanField(default=False)
    # read_time = models.IntegerField(default=0)

class Hackeathon(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    registration_start_date = models.DateField()
    registration_end_date = models.DateField()
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2)
    prize = models.DecimalField(max_digits=10, decimal_places=2)
    rules = models.TextField()
    eligibility = models.TextField()
    contact = models.TextField()
    link = models.TextField()
    # image = models.ImageField(upload_to='hackeathon/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='hackeathon_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='hackeathon_dislikes', blank=True)