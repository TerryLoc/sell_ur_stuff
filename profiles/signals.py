from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, Notification, Sale, Purchase


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=Purchase)
def notify_seller_purchase(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.sale.user,
            message=f"Your item '{instance.sale.title}' was sold to {instance.buyer.username}!",
        )
