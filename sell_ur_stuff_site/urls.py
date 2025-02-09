from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("sales/", include("sales.urls")),  # Include the sales app URLs
    path("market/", include("market.urls")),  # Marketplace URLs
    path("accounts/", include("allauth.urls")),  # Authentication URLs
    path("", include("home.urls")),  # Home page URL if you have one
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
