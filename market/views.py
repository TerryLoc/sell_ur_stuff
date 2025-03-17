from django.shortcuts import render
from sales.models import Sale


def market_list(request):
    """
    The list of all available products and display them in the market page.
    """
    products = Sale.objects.filter(status="available").order_by("-created_at")
    return render(request, "market/market.html", {"products": products})
