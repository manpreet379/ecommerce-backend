from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    store_name = models.CharField(max_length=255, blank=True)
    store_description = models.TextField(blank=True)
    store_address = models.CharField(max_length=255, blank=True)
    store_phone_number = models.CharField(max_length=20, blank=True)
    store_website = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.store_name} - {self.user.email}"
