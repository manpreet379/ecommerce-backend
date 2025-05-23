from rest_framework import serializers
from .models import Category, Product, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'created_at', 'updated_at', 'parent']
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_main']
        read_only_fields = ['id']


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = ['id', 'seller', 'name', 'description', 'price', 'category', 'brand', 'stock', 'images']
        read_only_fields = ['id', 'seller']
   
    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        product = Product.objects.create(**validated_data)
  
        for image_data in images_data:
            ProductImage.objects.create(product=product, **image_data)
        return product

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', None)
     
        instance = super().update(instance, validated_data)
        if images_data is not None:
            instance.images.all().delete()
            for image_data in images_data:
                ProductImage.objects.create(product=instance, **image_data)
