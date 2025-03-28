from django.contrib import admin
from .models import NewsletterSubscriber


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    """Register the NewsletterSubscriber model with the admin interface"""

    list_display = ("email", "subscribed_at", "is_active")
    list_filter = ("is_active", "subscribed_at")
    search_fields = ("email",)
