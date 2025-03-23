from django.db import models
from django.contrib.auth.models import User
from sales.models import Sale


class UserProfile(models.Model):
    """
    A model to store information about a user.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_picture = models.ImageField(
        upload_to="profile_pics/",
        blank=True,
        null=True,
        default="profile_pics/default.jpg",
    )
    location = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"  # Changed accordingly after testing


class Purchase(models.Model):
    """A model to store information about a purchase."""

    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="purchases")
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)
    price_paid = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )  # Add this

    def __str__(self):
        return f"{self.buyer.username} bought {self.sale.title}"


class Notification(models.Model):
    """A model to store notifications for users."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"
