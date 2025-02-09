from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Sale(models.Model):
    STATUS_CHOICES = [
        ("available", "Available"),
        ("sold", "Sold"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Seller
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="product_images/", blank=True, null=True)
    video = models.FileField(
        upload_to="product_videos/", blank=True, null=True
    )  # Video upload field
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="available"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
