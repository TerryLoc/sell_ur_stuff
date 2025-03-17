from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Sale(models.Model):
    STATUS_CHOICES = [
        ("available", "Available"),
        ("sold", "Sold"),
        ("pending", "Pending"),  # Pending approval by seller
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Seller
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    main_image = models.ImageField(
        upload_to="product_images/", blank=True, null=True
    )  # Main image
    image_1 = models.ImageField(upload_to="product_images/", blank=True, null=True)
    image_2 = models.ImageField(upload_to="product_images/", blank=True, null=True)
    image_3 = models.ImageField(upload_to="product_images/", blank=True, null=True)
    video = models.FileField(
        upload_to="product_videos/", blank=True, null=True
    )  # Video upload field
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="available"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Offer(models.Model):
    """
    Model for offers made by users on sale items by sellers (users) on sale items with the ability to accept or reject offers
    """

    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="offers")
    buyer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="offers_made"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        default="pending",
        choices=[
            ("pending", "Pending"),
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
        ],
    )
    counter_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    # Counter offer status to be used by the seller to send a counter offer to the buyer
    counter_status = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        choices=[
            ("pending", "Pending"),
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Offer of €{self.amount} on {self.sale.title} by {self.buyer.username}"
