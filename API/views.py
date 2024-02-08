from rest_framework import generics
from API.models import UserProfile, UserPost, Hackeathon, UserComment
from API.serializers import UserProfileSerializer,UserRegistrationSerializer, UserPostSerializer, HackeathonSerializer, UserCommentSerializer
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import FileUploadParser
from rest_framework_simplejwt.views import TokenObtainPairView
from API.serializers import CustomTokenObtainPairSerializer
from django.contrib.auth.hashers import make_password


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Hash the password before saving the user
        validated_data = serializer.validated_data
        validated_data['password'] = make_password(validated_data['password'])
        user = serializer.save()
        refresh = CustomTokenObtainPairSerializer().get_token(user)
        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
        }
        UserProfile.objects.create(user=user)
        return Response(response_data, status=status.HTTP_201_CREATED)
    

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


class UserProfileDetail(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)

    def put(self, request, *args, **kwargs):
        user_profile = self.get_object()
        serializer = UserProfileSerializer(user_profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# class UserLogoutView(APIView):
#     def post(self, request):
#         try:
#             refresh_token = request.data['refresh']
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#             return Response({'detail': 'Token successfully blacklisted'}, status=200)
#         except Exception as e:
#             return Response({'detail': str(e)}, status=400)
        

from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

class UserLogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            jti = token['jti']
            OutstandingToken.objects.filter(jti=jti).delete()
            BlacklistedToken.objects.create(token=token)
            return Response({'detail': 'Token successfully blacklisted'}, status=200)
        except Exception as e:
            return Response({'detail': str(e)}, status=400)
        


class UserPostView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserPostSerializer

    def get_queryset(self):
        return UserPost.objects.filter(deleted=False).order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk, *args, **kwargs):
        try:
            post = UserPost.objects.get(pk=pk)
        except UserPost.DoesNotExist:
            return Response({'detail': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        if post.user != request.user:
            return Response({'detail': 'You do not have permission to edit this post'}, status=status.HTTP_403_FORBIDDEN)
        serializer = UserPostSerializer(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, *args, **kwargs):
        try:
            post = UserPost.objects.get(pk=pk)
        except UserPost.DoesNotExist:
            return Response({'detail': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        if post.user != request.user:
            return Response({'detail': 'You do not have permission to delete this post'}, status=status.HTTP_403_FORBIDDEN)
        post.deleted = True
        post.save()
        return Response({'detail': 'Post successfully deleted'}, status=status.HTTP_204_NO_CONTENT)


class HackeathonView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = HackeathonSerializer

    def get_queryset(self):
        return Hackeathon.objects.all().order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def put(self, request, pk, *args, **kwargs):
        try:
            hackeathon = Hackeathon.objects.get(pk=pk)
        except Hackeathon.DoesNotExist:
            return Response({'detail': 'Hackeathon not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = HackeathonSerializer(hackeathon, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk, *args, **kwargs):
        try:
            hackeathon = Hackeathon.objects.get(pk=pk)
        except Hackeathon.DoesNotExist:
            return Response({'detail': 'Hackeathon not found'}, status=status.HTTP_404_NOT_FOUND)
        hackeathon.delete()
        return Response({'detail': 'Hackeathon successfully deleted'}, status=status.HTTP_204_NO_CONTENT)
    
class UserCommentView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserCommentSerializer

    def get_queryset(self):
        return UserComment.objects.all().order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def put(self, request, pk, *args, **kwargs):
        try:
            comment = UserComment.objects.get(pk=pk)
        except UserComment.DoesNotExist:
            return Response({'detail': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
        if comment.user != request.user:
            return Response({'detail': 'You do not have permission to edit this comment'}, status=status.HTTP_403_FORBIDDEN)
        serializer = UserCommentSerializer(comment, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk, *args, **kwargs):
        try:
            comment = UserComment.objects.get(pk=pk)
        except UserComment.DoesNotExist:
            return Response({'detail': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
        if comment.user != request.user:
            return Response({'detail': 'You do not have permission to delete this comment'}, status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response({'detail': 'Comment successfully deleted'}, status=status.HTTP_204_NO_CONTENT)
    
    def post(self, request, *args, **kwargs):
        serializer = UserCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)