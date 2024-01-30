from django.urls import path
from API.views import UserProfileDetail, VerifyTokenView, UserRegistrationView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/verify/', VerifyTokenView.as_view(), name='verify-token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('profile/', UserProfileDetail.as_view(), name='user-profile-detail'),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
]
