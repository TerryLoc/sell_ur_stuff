from django.db import models


class NewsletterSubscriber(models.Model):
    """Model to store newsletter subscribers"""

    email = models.EmailField(unique=True, max_length=255)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email

    class Meta:
        """Meta class for the model"""

        verbose_name = "Newsletter Subscriber"
        verbose_name_plural = "Newsletter Subscribers"
        ordering = ("-subscribed_at",)
