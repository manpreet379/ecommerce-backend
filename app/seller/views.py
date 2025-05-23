from .serializers import SellerProfileSerializer
from rest_framework.views import APIView
from .models import SellerProfile
from utils.responder import ResponseBuilder
from rest_framework.permissions import IsAuthenticated


class SellerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Fetch the seller profile for the current user
        seller_profile = SellerProfile.objects.get(user=request.user)
        serializer = SellerProfileSerializer(seller_profile)
        return ResponseBuilder.ok(
            code=147,
            data=serializer.data
        )

    def put(self, request):
       
        seller_profile = SellerProfile.objects.get(user=request.user)
        serializer = SellerProfileSerializer(seller_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return ResponseBuilder.accepted(
                code=148,
                data=serializer.data
            )
        return ResponseBuilder.bad_request(
            code=149,
            errors=serializer.errors
        )