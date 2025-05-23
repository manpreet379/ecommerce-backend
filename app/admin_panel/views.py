from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model
from .serializers import SellerApprovalSerializer
from utils.responder import ResponseBuilder
from django.shortcuts import get_object_or_404

User = get_user_model()


class PendingSellerListAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        pending_sellers = User.objects.filter(role='seller', is_approved=False)
        serializer = SellerApprovalSerializer(pending_sellers, many=True)
        return ResponseBuilder.ok(
            code=142,
            data=serializer.data
        )


class ApproveSellerAPIView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        seller = get_object_or_404(User, pk=pk, role='seller' )
        if seller.is_approved:
            return ResponseBuilder.bad_request(
                code=143,
                
            )
        seller.is_approved = True
        seller.save()
        serializer = SellerApprovalSerializer(seller)
        return ResponseBuilder.accepted(
            code=144,
            data=serializer.data
        )
        

class RejectSellerAPIView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        seller = get_object_or_404(User, pk=pk, role='seller')
        if not seller.is_approved:
            return ResponseBuilder.bad_request(
                code=145,
                
            )
        seller.is_approved = False
        seller.save()
        serializer = SellerApprovalSerializer(seller)
        return ResponseBuilder.accepted(
            code=146,
            data=serializer.data
        )
