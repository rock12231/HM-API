# myapp/serializers.py

from rest_framework import serializers
from API.models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('bio',)
