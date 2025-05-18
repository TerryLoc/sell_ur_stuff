from django.contrib import admin
from .models import Sale, Offer, Purchase  # Import Purchase model

admin.site.register(Sale)
admin.site.register(Offer)
admin.site.register(Purchase)  # Register Purchase model
