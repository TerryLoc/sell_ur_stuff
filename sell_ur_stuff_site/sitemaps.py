from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from sales.models import Sale
from profiles.models import UserProfile


class StaticSitemap(Sitemap):
    # Add this class to generate sitemap for static pages
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        # Return list of url names - use your actual URL names here
        return ["home", "market_list", "contact"]

    def location(self, item):
        return reverse(item)


class SaleSitemap(Sitemap):
    # Add this class to generate sitemap for sales
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Sale.objects.filter(status="active")

    def location(self, obj):
        return reverse("sale_detail", args=[obj.id])

    def lastmod(self, obj):
        return obj.updated_at


class ProfileSitemap(Sitemap):
    # Add this class to generate sitemap for user profiles
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return UserProfile.objects.all()

    def location(self, obj):
        return reverse("profile")

    def lastmod(self, obj):
        return obj.user.date_joined
