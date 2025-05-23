from rest_framework import serializers
from .models import SellerProfile


class SellerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model= SellerProfile
        fields='__all__'
        read_only_fields=['id', 'user', 'created_at', 'updated_at']
        
        