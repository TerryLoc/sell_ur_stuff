from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Purchase, Notification


# Define an inline admin descriptor for UserProfile
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "User Profiles"


# Define a new User admin
class CustomUserAdmin(UserAdmin):
    # Customize fieldsets without duplicating fields
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "email")},
        ),  # Already includes first_name and last_name
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    # Display these fields in the list view
    list_display = ("username", "email", "first_name", "last_name", "is_staff")
    # Add the inline
    inlines = (UserProfileInline,)


# Unregister the default User admin and register the custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Register other models
admin.site.register(UserProfile)
admin.site.register(Purchase)
admin.site.register(Notification)
