from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "name", "email", "created_at", "is_resolved")
    list_filter = ("is_resolved", "created_at")
    search_fields = ("subject", "name", "email", "message")
    actions = ["mark_as_resolved"]

    def mark_as_resolved(self, request, queryset):
        queryset.update(is_resolved=True)

    mark_as_resolved.short_description = "Mark selected messages as resolved"
