import base64
from django.http import HttpResponse
from rest_framework import generics
from API.models import ProfileModel, CommentModel, PostModel, HackeathonModel, ForgotPasswordModel
from API.serializers import PostSerializer, CommentSerializer, ProfileSerializer, HackeathonSerializer, CustomTokenObtainPairSerializer, RegistrationSerializer, LikeSerializer,PostCreateSerializer
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import FileUploadParser
from rest_framework_simplejwt.views import TokenObtainPairView
from API.serializers import CustomTokenObtainPairSerializer,ForgotPasswordSerializer,ResetPasswordSerializer,ProfilePhotoSerializer
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.hashers import make_password
import random
from django.core.mail import send_mail
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework import viewsets


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


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


class RegistrationAPIView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
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
        ProfileModel.objects.create(user=user)
        return Response(response_data, status=status.HTTP_201_CREATED)


class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        email = request.data.get('email')
        print(email, User.objects.filter(email=email))
        if User.objects.filter(email=email).exists():
            print("user exists")
            otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            print(otp)
            create_otp = ForgotPasswordModel.objects.create(email=email, otp=otp)
            create_otp.save()
            # Send OTP via email
            # send_mail(
            #     'Your OTP for Password Reset',
            #     f'Your OTP is {otp}',
            #     'your@example.com',
            #     [email],
            #     fail_silently=False,
            # )
            print("mail sent")
            return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)
        

class ResetPasswordView(APIView):
    serializer_class = ResetPasswordSerializer
    
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        new_password = request.data.get('new_password')
        # check time limit from the time of otp creation 10 minutes
        last_otp_instance = ForgotPasswordModel.objects.filter(email=email).order_by('-created_at').first()
        print(last_otp_instance.email, last_otp_instance.otp, last_otp_instance.created_at, last_otp_instance.updated_at)
        if last_otp_instance and int(last_otp_instance.otp) != otp:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        # Check if OTP is valid and creation time is within 10 minutes
        if last_otp_instance.created_at + timedelta(minutes=10) < timezone.now():
            return Response({'error': 'OTP has expired'}, status=status.HTTP_400_BAD_REQUEST)

        # OTP is valid and within time limit, proceed with password reset
        # Update user's password
        try:
            user = User.objects.get(email=email)
            user.password = make_password(new_password)
            print(user.password)
            user.save()
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Clear OTP from database
        last_otp_instance.otp = ''
        last_otp_instance.save()

        return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_object(self):
        return ProfileModel.objects.get(user=self.request.user)

    def put(self, request, *args, **kwargs):
        user_profile = self.get_object()
        first_name= request.data.get('first_name')
        last_name= request.data.get('last_name')
        user = user_profile.user
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        serializer = ProfileSerializer(user_profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfilePhotoAPIView(APIView):
    parser_class = (FileUploadParser,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfilePhotoSerializer

    # convert the image to base64 and send it to the server
    def convert_base64(self, image):
        return base64.b64encode(image.read()).decode('utf-8')
    
    def get(self, request, *args, **kwargs):
        user_profile = ProfileModel.objects.get(user=request.user)
        avatar = user_profile.avatar
        if avatar:
            return Response({'avatar': self.convert_base64(avatar)}, status=status.HTTP_200_OK)
        return Response({'avatar': None}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user_profile = ProfileModel.objects.get(user=request.user)
        user_profile.avatar = request.data['avatar']
        user_profile.save()
        return Response({'detail': 'Profile photo updated successfully'}, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            print(refresh_token)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': 'User Logout'},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': 'Error'},status=status.HTTP_400_BAD_REQUEST)


class PostAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return PostModel.objects.filter(deleted=False).order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk, *args, **kwargs):
        try:
            post = PostModel.objects.get(pk=pk)
        except PostModel.DoesNotExist:
            return Response({'detail': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        if post.user != request.user:
            return Response({'detail': 'You do not have permission to edit this post'}, status=status.HTTP_403_FORBIDDEN)
        serializer = PostSerializer(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, *args, **kwargs):
        try:
            post = PostModel.objects.get(pk=pk)
        except PostModel.DoesNotExist:
            return Response({'detail': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        if post.user != request.user:
            return Response({'detail': 'You do not have permission to delete this post'}, status=status.HTTP_403_FORBIDDEN)
        post.deleted = True
        post.save()
        return Response({'detail': 'Post successfully deleted'}, status=status.HTTP_204_NO_CONTENT)


class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = PostModel.objects.all()
    serializer_class = PostCreateSerializer

    def get(self, request, pk, *args, **kwargs):
        try:
            post = PostModel.objects.get(pk=pk)
        except PostModel.DoesNotExist:
            return Response({'detail': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostCreateSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request, pk, *args, **kwargs):
        try:
            post = PostModel.objects.get(pk=pk)
        except PostModel.DoesNotExist:
            return Response({'detail': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostCreateSerializer(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk, *args, **kwargs):
        try:
            post = PostModel.objects.get(pk=pk)
        except PostModel.DoesNotExist:
            return Response({'detail': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostCreateSerializer(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk, *args, **kwargs):
        try:
            post = PostModel.objects.get(pk=pk)
        except PostModel.DoesNotExist:
            return Response({'detail': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        post.deleted = True
        post.save()
        return Response({'detail': 'Post successfully deleted'}, status=status.HTTP_204_NO_CONTENT)


class PostSearchAPIView(generics.ListAPIView):
    queryset = PostModel.objects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content', 'types']  # Define fields to search

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Check if 'types' parameter exists in the request
        types_filter = request.query_params.get('types')

        if types_filter:
            queryset = queryset.filter(types=types_filter)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

class LikePostAPIView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LikeSerializer
    
    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)
    
    def post(self, request, pk, *args, **kwargs):
        try:
            post = PostModel.objects.get(pk=pk)
            print(post.id, post.title, post.content, post.likes.all())
        except PostModel.DoesNotExist:
            return Response({'detail': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user in post.likes.all():
            # If the user has already liked the post, unlike it
            post.likes.remove(request.user)
            liked = False
        else:
            # If the user hasn't liked the post, like it
            post.likes.add(request.user)
            liked = True
        
        post.save()
        serializer = self.get_serializer(post)
        return Response({'liked': liked, 'likes_count': post.likes.count()}, status=status.HTTP_200_OK)


class HackeathonAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = HackeathonSerializer

    def get_queryset(self):
        return HackeathonModel.objects.all().order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def put(self, request, pk, *args, **kwargs):
        try:
            hackeathon = HackeathonModel.objects.get(pk=pk)
        except HackeathonModel.DoesNotExist:
            return Response({'detail': 'Hackeathon not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = HackeathonSerializer(hackeathon, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk, *args, **kwargs):
        try:
            hackeathon = HackeathonModel.objects.get(pk=pk)
        except HackeathonModel.DoesNotExist:
            return Response({'detail': 'Hackeathon not found'}, status=status.HTTP_404_NOT_FOUND)
        hackeathon.delete()
        return Response({'detail': 'Hackeathon successfully deleted'}, status=status.HTTP_204_NO_CONTENT)
    

class CommentAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer

    def get_queryset(self):
        return CommentModel.objects.all().order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def put(self, request, pk, *args, **kwargs):
        try:
            comment = CommentModel.objects.get(pk=pk)
        except CommentModel.DoesNotExist:
            return Response({'detail': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
        if comment.user != request.user:
            return Response({'detail': 'You do not have permission to edit this comment'}, status=status.HTTP_403_FORBIDDEN)
        serializer = CommentSerializer(comment, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk, *args, **kwargs):
        try:
            comment = CommentModel.objects.get(pk=pk)
        except CommentModel.DoesNotExist:
            return Response({'detail': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
        if comment.user != request.user:
            return Response({'detail': 'You do not have permission to delete this comment'}, status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response({'detail': 'Comment successfully deleted'}, status=status.HTTP_204_NO_CONTENT)
    
    def post(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class LikeCommentAPIView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LikeSerializer

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)
    
    def post(self, request, pk, *args, **kwargs):
        try:
            comment = CommentModel.objects.get(pk=pk)
        except CommentModel.DoesNotExist:
            return Response({'detail': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user in comment.likes.all():
            # If the user has already liked the comment, unlike it
            comment.likes.remove(request.user)
            liked = False
        else:
            # If the user hasn't liked the comment, like it
            comment.likes.add(request.user)
            liked = True
        
        comment.save()
        serializer = self.get_serializer(comment)
        return Response({'liked': liked, 'likes_count': comment.likes.count()}, status=status.HTTP_200_OK)
    