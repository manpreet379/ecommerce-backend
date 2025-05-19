from .serializers import CategorySerializer
from rest_framework.views import APIView
from .models import Category
from rest_framework import status
from utils.responder import standard_response
from .permissions import IsAdminOrReadonly

class CategoryListCreateAPIView(APIView):
    permission_classes = [IsAdminOrReadonly]
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return standard_response(
            status_code=status.HTTP_200_OK,
            message="Category list fetched successfully.",
            data=serializer.data
        )
    
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return standard_response(
                status_code=status.HTTP_201_CREATED,
                message="Category created successfully.",
                data=serializer.data
            )
        return standard_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            status="error",
            message="Category creation failed.",
            data=serializer.errors
        )




