import stripe
from django.conf import settings

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Sale
from .forms import SaleForm
from profiles.models import Notification, Purchase

# The secret key for the Stripe API
stripe.api_key = settings.STRIPE_SECRET_KEY


# This is so the user can only see their own sales listings
@login_required
def sales_list(request):
    """
    List all sales for the logged-in user that are available
    """
    sales = Sale.objects.filter(
        user=request.user, status="available"
    )  # Only available items
    return render(request, "sales/sales_list.html", {"sales": sales})


# View details of a single sale
def sale_detail(request, sale_id):
    """
    View details of a single sale listing
    """
    sale = get_object_or_404(Sale, id=sale_id)
    return render(request, "sales/sale_detail.html", {"sale": sale})


# Create a new sale
@login_required
def sale_create(request):
    """
    Create a new sale listing and save it to the database
    """
    if request.method == "POST":
        form = SaleForm(request.POST, request.FILES)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.user = request.user
            sale.save()
            return redirect("sales_list")
    else:
        form = SaleForm()
    return render(request, "sales/sale_form.html", {"form": form})


# Update an existing sale
@login_required
def sale_update(request, sale_id):
    """
    Update an existing sale listing ie. change the details of a sale
    """
    sale = get_object_or_404(Sale, id=sale_id, user=request.user)
    if sale.status == "sold":
        return redirect("sales_list")  # Or render an error page
    if request.method == "POST":
        form = SaleForm(request.POST, request.FILES, instance=sale)
        if form.is_valid():
            form.save()
            return redirect("sales_list")
    else:
        form = SaleForm(instance=sale)
    return render(request, "sales/sale_form.html", {"form": form})


# Delete a sale
@login_required
def sale_delete(request, sale_id):
    """
    Delete a sale listing from the database and redirect to the sales list of the user
    """
    sale = get_object_or_404(Sale, id=sale_id, user=request.user)
    if sale.status == "sold":
        return redirect("sales_list")  # Or render an error page
    if request.method == "POST":
        sale.delete()
        return redirect("sales_list")
    return render(request, "sales/sale_confirm_delete.html", {"sale": sale})


# Buy a product
@login_required
def buy_product(request, sale_id):
    """
    Buy a product using the Stripe API and redirect to the payment page on Stripe
    """
    sale = get_object_or_404(Sale, id=sale_id)
    if sale.status != "available":
        return redirect("market_list")
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "eur",
                    "product_data": {"name": sale.title},
                    "unit_amount": int(sale.price * 100),
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=request.build_absolute_uri("/sales/success/")
        + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri("/sales/cancel/"),
        metadata={"sale_id": sale.id},
    )
    return redirect(session.url, code=303)


# Payment success and cancel views
def payment_success(request):
    """
    Payment success view that triggers a notification to the seller
    """
    session_id = request.GET.get("session_id")
    session = stripe.checkout.Session.retrieve(session_id)
    sale = get_object_or_404(Sale, id=session.metadata["sale_id"])
    # If the payment was successful, change the status of the sale to sold
    if session.payment_status == "paid":
        sale.status = "sold"
        sale.save()
        Purchase.objects.create(buyer=request.user, sale=sale)  # Triggers notification
    return render(request, "sales/payment_result.html", {"success": True, "sale": sale})


# Payment cancel view
def payment_cancel(request):
    """
    Payment cancel view that redirects to the payment result page with a failure message
    """
    return render(request, "sales/payment_result.html", {"success": False})
