from django.shortcuts import render, redirect, get_object_or_404
from sales.models import Sale


def market_list(request):
    """
    The list of all available products and display them in the market
    """
    products = Sale.objects.filter(status="available")  # Only show available items
    return render(request, "market/market.html", {"products": products})
