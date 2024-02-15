# myapp/serializers.py

from rest_framework import serializers
from API.models import ProfileModel, CommentModel, PostModel, HackeathonModel, ForgotPasswordModel
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


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # Revome password validation
    def validate_password(self, value):
        return value
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    # class Meta:
    #     model = ForgotPasswordModel
    #     fields = '__all__'


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
    password = serializers.CharField()
    # class Meta:
    #     model = ForgotPasswordModel
    #     fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', required=False)  # Update to allow partial updates
    last_name = serializers.CharField(source='user.last_name', required=False)  # Update to allow partial updates
    last_login = serializers.DateTimeField(source='user.last_login', read_only=True)
    date_joined = serializers.DateTimeField(source='user.date_joined', read_only=True)

    class Meta:
        model = ProfileModel
        fields = ['username', 'email', 'first_name', 'last_name', 'last_login', 'date_joined',
                  'bio', 'college', 'branch', 'year', 'batch', 'occupation', 'githublink',
                  'linkedinlink', 'twitterlink', 'instagramlink', 'facebooklink', 'stackoverflowlink',
                  'otherlink','gender']

    def update(self, instance, validated_data):
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
        instance.gender = validated_data.get('gender', instance.gender)
        instance.save()
        return instance


class ProfilePhotoSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField()

    class Meta:
        model = ProfileModel
        fields = ['avatar']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_dislike_count(self, obj):
        return obj.dislikes.count()
    
    class Meta:
        model = CommentModel
        fields = ['id', 'user', 'post', 'content', 'created_at', 'updated_at', 'like_count', 'dislike_count']


class PostSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    like_count = serializers.SerializerMethodField()

    def get_like_count(self, obj):
        return obj.likes.count()

    
    class Meta:
        model = PostModel
        fields = ['id', 'user','hackeathon','likes', 'types', 'title', 'content','member','created_at', 'updated_at', 'like_count']


class PostCreateSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True, source='commentmodel_set')
    intrested = serializers.SerializerMethodField()

    def get_like_count(self, obj):
        return obj.likes.count()
    
    def get_comment_count(self, obj):
        return obj.comments.count()
    
    def get_intrested(self, obj):
        return obj.intrested.count()
    
    def get_comments(self, obj):
        return CommentSerializer(obj.comments.all(), many=True).data
    
    class Meta:
        model = PostModel
        fields = ['id', 'user','hackeathon','likes', 'types', 'title', 'content','member','created_at', 'updated_at', 'like_count', 'comment_count','comments','intrested']


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = PostModel
        fields = ['likes', 'user']


class HackeathonSerializer(serializers.ModelSerializer):
    class Meta:
        model = HackeathonModel
        fields = '__all__'