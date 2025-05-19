from django.urls import path
from .views import LogoutView, UserListCreateAPIView, PasswordResetRequestView,ResetPasswordConfirmView, AddressListCreateAPIView, AddressDetailAPIView,UserProfileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns=[
    path('register/', UserListCreateAPIView.as_view(), name='user-list-create'),
    path('login/',TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/',LogoutView.as_view(), name='logout'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('reset-password-confirm/', ResetPasswordConfirmView.as_view(), name='reset-password-confirm'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('address/', AddressListCreateAPIView.as_view(), name='address-list-create'),
    path('address/<int:pk>/', AddressDetailAPIView.as_view(), name='address-detail'),
]