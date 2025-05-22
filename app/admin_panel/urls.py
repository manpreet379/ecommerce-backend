from django.urls import path
from .views import PendingSellerListAPIView, ApproveSellerAPIView, RejectSellerAPIView

urlpatterns = [
    path('pending-sellers/', PendingSellerListAPIView.as_view(), name='pending-sellers'),
    path('approve-seller/<int:pk>/', ApproveSellerAPIView.as_view(), name='approve-seller'),
    path('reject-seller/<int:pk>/', RejectSellerAPIView.as_view(), name='reject-seller'),
]