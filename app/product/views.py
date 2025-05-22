from .serializers import CategorySerializer, ProductSerializer
from rest_framework.views import APIView
from .models import Category, Product
from utils.responder import ResponseBuilder
from .permissions import IsAdminOrReadonly, IsSellerOrReadonly, IsProductOwner
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


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


class ProductListCreateAPIView(APIView):
    permission_classes = [IsSellerOrReadonly]
  
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return ResponseBuilder.ok(
            code=133,
            data=serializer.data
        )
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(seller=request.user)
            return ResponseBuilder.accepted(
                code=134,
                data=serializer.data
            )
        return ResponseBuilder.bad_request(
            code=135,
            errors=serializer.errors
        )


class ProductDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsProductOwner]
    
    def get_object(self, pk):
        """Helper method to get a product instance or raise 404."""
        return get_object_or_404(Product, pk=pk)
    
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        self.check_object_permissions(request, product)
        serializer = ProductSerializer(product)
        return ResponseBuilder.ok(
            code=136,
            data=serializer.data
        )
        
    def put(self, request, pk):
        product = self.get_object(pk)
        self.check_object_permissions(request, product)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return ResponseBuilder.ok(
                code=137,
                data=serializer.data
            )
        return ResponseBuilder.bad_request(
            code=138,
            errors=serializer.errors
        )
    
    def delete(self, request, pk):
       
        product = self.get_object(pk)
       
        self.check_object_permissions(request, product)
        product.delete()
        return ResponseBuilder.not_found(
            code=139
        )
        
