from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class SellerApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'role', 'is_approved']
        read_only_fields = ['id', 'email', 'role', 'full_name']
        