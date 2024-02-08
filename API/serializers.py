# myapp/serializers.py

from rest_framework import serializers
from API.models import UserProfile, UserComment, UserPost, Hackeathon
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        return token

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # Revome password validation
    def validate_password(self, value):
        return value
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    last_login = serializers.DateTimeField(source='user.last_login', read_only=True)
    date_joined = serializers.DateTimeField(source='user.date_joined', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = '__all__'

    # def create(self, validated_data):
    #     user_data = validated_data.pop('user')
    #     user = User.objects.create_user(**user_data)
    #     profile = UserProfile.objects.create(user=user, **validated_data)
    #     return profile
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user
        instance.bio = validated_data.get('bio', instance.bio)
        instance.college = validated_data.get('college', instance.college)
        instance.branch = validated_data.get('branch', instance.branch)
        instance.year = validated_data.get('year', instance.year)
        instance.batch = validated_data.get('batch', instance.batch)
        instance.occupation = validated_data.get('occupation', instance.occupation)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.githublink = validated_data.get('githublink', instance.githublink)
        instance.linkedinlink = validated_data.get('linkedinlink', instance.linkedinlink)
        instance.twitterlink = validated_data.get('twitterlink', instance.twitterlink)
        instance.instagramlink = validated_data.get('instagramlink', instance.instagramlink)
        instance.facebooklink = validated_data.get('facebooklink', instance.facebooklink)
        instance.stackoverflowlink = validated_data.get('stackoverflowlink', instance.stackoverflowlink)
        instance.otherlink = validated_data.get('otherlink', instance.otherlink)
        instance
        user.username = user_data.get('username', user.username)
        user.email = user_data.get('email', user.email)
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.save()
        instance.save()
        return instance

class UserCommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_dislike_count(self, obj):
        return obj.dislikes.count()
    
    class Meta:
        model = UserComment
        fields = ['id', 'user', 'post', 'content', 'created_at', 'updated_at', 'like_count', 'dislike_count']

class UserPostSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_comment_count(self, obj):
        return obj.comments.count()
    
    class Meta:
        model = UserPost
        fields = ['id', 'user','hackeathon', 'types', 'title', 'content', 'created_at', 'updated_at', 'like_count', 'comment_count']

class HackeathonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hackeathon
        fields = '__all__'