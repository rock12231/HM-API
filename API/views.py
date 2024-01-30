from rest_framework import generics
from API.models import UserProfile
from API.serializers import UserProfileSerializer,UserRegistrationSerializer
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken



class UserProfileDetail(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)

@authentication_classes([])
@permission_classes([])
class VerifyTokenView(APIView):
    def get(self, request, *args, **kwargs):
        authorization_header = request.headers.get('Authorization')

        if not authorization_header or not authorization_header.startswith('Bearer '):
            return Response({'detail': 'Invalid Authorization header'}, status=401)

        token = authorization_header.split(' ')[1]

        try:
            # Decode the token
            decoded_token = AccessToken(token)
            user = decoded_token.payload.get('user_id')
            # Now 'user' contains the user ID or None if the token is invalid/expired
            # You can use it as needed, for example, to get user information from the database
            # check user is in database
            # if not user in UserProfile.objects.all():
            #     return Response({'detail': 'Invalid token'}, status=401)
            return Response({'user_id': user}, status=200)
        except Exception as e:
            return Response({'detail': str(e)}, status=401)


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(response_data, status=status.HTTP_201_CREATED)