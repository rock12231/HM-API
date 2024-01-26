from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from API.models import UserProfile
from API.serializers import UserProfileSerializer

class UserProfileDetail(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)
