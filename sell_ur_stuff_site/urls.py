from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from allauth.account.views import LoginView, SignupView


urlpatterns = [
    # Override Allauth's login and signup views
    path(
        "account/login/",
        LoginView.as_view(template_name="account/login.html"),
        name="account_login",
    ),
    path(
        "account/signup/",
        SignupView.as_view(template_name="account/signup.html"),
        name="account_signup",
    ),
    path("accounts/", include("allauth.urls")),
    # Admin URL and other app URLs
    path("admin/", admin.site.urls),
    path("", include("home.urls")),  # Home page URL if you have one
    path("market/", include("market.urls")),  # Marketplace URLs
    path("sales/", include("sales.urls")),  # Include the sales app URLs
    path("profiles/", include("profiles.urls")),  # Include the profiles app URLs
    path("contact/", include("contact.urls")),  # Include the contact app URLs
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
