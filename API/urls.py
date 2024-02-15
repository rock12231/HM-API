from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from API.views import RegistrationAPIView,PostSearchAPIView,ProfileAPIView,LikePostAPIView,PostAPIView
from API.views import LogoutAPIView, CustomTokenObtainPairView, VerifyTokenView, HackeathonAPIView
from API.views import PostDetailAPIView,ForgotPasswordView,ResetPasswordView,ProfilePhotoAPIView

urlpatterns = [
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/verify/', VerifyTokenView.as_view(), name='verify_token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('forgotpassword/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('resetpassword/', ResetPasswordView.as_view(), name='reset_password'),

    path('logout/', LogoutAPIView.as_view(), name='token_logout'),

    path('register/', RegistrationAPIView.as_view(), name='registration'),
    path('profile/', ProfileAPIView.as_view(), name='profile_detail'),
    path('profile/photo/', ProfilePhotoAPIView.as_view(), name='profile_photo'),

    path('hackeathon/', HackeathonAPIView.as_view(), name='hackeathon'),

    path('post/', PostAPIView.as_view(), name='post'),
    path('post/<int:pk>/', PostAPIView.as_view(), name='post_detail'),
    path('post/like/<int:pk>/', LikePostAPIView.as_view(), name='like_post'),
    path('post/search/', PostSearchAPIView.as_view(), name='post_search'),

    path('post/show/<int:pk>/', PostDetailAPIView.as_view(), name='post_show'),

]
