from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import SellerProfile

User= get_user_model()
@receiver(post_save, sender=User)
def create_seller_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'seller':
        SellerProfile.objects.create(user=instance)