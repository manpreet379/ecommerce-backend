from .serializers import CategorySerializer
from rest_framework.views import APIView
from .models import Category
from utils.responder import ResponseBuilder
from .permissions import IsAdminOrReadonly


class CategoryListCreateAPIView(APIView):
    permission_classes = [IsAdminOrReadonly]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return ResponseBuilder.ok(
            code=130,
            data=serializer.data
        )

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseBuilder.accepted(
                code=131,
                data=serializer.data
            )
        return ResponseBuilder.bad_request(
            code=132,
            errors=serializer.errors
        )
