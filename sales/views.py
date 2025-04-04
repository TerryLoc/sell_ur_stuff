import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from profiles.models import Purchase, Notification
from .models import Sale, Offer
from .forms import SaleForm, OfferForm, CounterOfferForm
from django.contrib import messages

# The secret key for the Stripe API
stripe.api_key = settings.STRIPE_SECRET_KEY


# This is so the user can only see their own sales listings
@login_required
def sales_list(request):
    """
    List all sales for the logged-in user, categorized by status: available, sold, or pending.
    """
    # Active sales are sales that are available for purchase
    active_sales = Sale.objects.filter(user=request.user, status="available").order_by(
        "-created_at"
    )
    # Sold purchases are sales that have been marked as sold
    sold_purchases = (
        Purchase.objects.filter(sale__user=request.user)
        .select_related("sale")
        .order_by("-purchased_at")
    )
    # Pending sales are offers that have been accepted but not yet paid for
    pending_sales = Sale.objects.filter(user=request.user, status="pending").order_by(
        "-created_at"
    )
    return render(
        request,
        "sales/sales_list.html",
        {
            "active_sales": active_sales,
            "sold_purchases": sold_purchases,
            "pending_sales": pending_sales,
        },
    )


# View details of a single sale
def sale_detail(request, sale_id):
    """
    View details of a single sale listing with the option to buy the product or make an offer
    """
    sale = get_object_or_404(Sale, id=sale_id)
    purchase = None
    highest_offer = (
        Offer.objects.filter(sale=sale, status="pending").order_by("-amount").first()
    )
    accepted_offer = None

    if sale.status == "sold" and request.user.is_authenticated:
        purchase = Purchase.objects.filter(sale=sale, buyer=request.user).first()
        # Get the accepted/paid offer if the item is sold
        accepted_offer = Offer.objects.filter(
            sale=sale, status__in=["accepted", "paid"]
        ).first()

    return render(
        request,
        "sales/sale_detail.html",
        {
            "sale": sale,
            "purchase": purchase,
            "highest_offer": highest_offer,
            "offer": accepted_offer,  # To pass the accepted offer to the template
        },
    )


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
    Payment success view that triggers a notification to the seller and marks the sale as sold
    """
    session_id = request.GET.get("session_id")
    session = stripe.checkout.Session.retrieve(session_id)
    sale = get_object_or_404(Sale, id=session.metadata["sale_id"])
    if session.payment_status == "paid":
        sale.status = "sold"
        sale.save()
        Purchase.objects.create(
            buyer=request.user,
            sale=sale,
            price_paid=sale.price,  # Set to listed price for direct buys
        )  # Triggers notification
    return render(request, "sales/payment_result.html", {"success": True, "sale": sale})


def payment_cancel(request):
    """
    Payment cancel view that redirects to the payment result page with a failure message
    """
    return render(request, "sales/payment_result.html", {"success": False})


# Offer views for buyers and sellers to make and accept/reject offers on sale items
@login_required
def make_offer(request, sale_id):
    """
    Make an offer on a sale item listing by a user (buyer) on a sale item
    """
    sale = get_object_or_404(Sale, id=sale_id)
    if sale.status != "available":
        return redirect("market_list")
    if request.method == "POST":
        form = OfferForm(request.POST, sale=sale)  # Pass sale here
        if form.is_valid():
            offer = form.save(commit=False)
            offer.sale = sale
            offer.buyer = request.user
            offer.save()
            Notification.objects.create(
                user=sale.user,
                message=f"New offer of €{offer.amount} on your item '{sale.title}' from {request.user.username}!",
            )
            return redirect("sale_detail", sale_id=sale.id)
    else:
        form = OfferForm(sale=sale)  # Pass sale here
    return render(request, "sales/make_offer.html", {"sale": sale, "form": form})


@login_required
def seller_offers(request):
    """
    List all offers made on the sales listings of the logged-in user
    """
    offers = Offer.objects.filter(sale__user=request.user).order_by("-created_at")
    return render(request, "sales/seller_offers.html", {"offers": offers})


@login_required
def accept_offer(request, offer_id):
    """Accept an offer on a sale item listing by a user (buyer) on a sale item"""
    offer = get_object_or_404(Offer, id=offer_id, sale__user=request.user)
    if offer.status != "pending":
        return redirect("profile")
    offer.status = "accepted"
    offer.save()
    sale = offer.sale
    sale.status = "pending"  # Mark as pending until payment is completed
    sale.save()
    # Notify buyer that their offer was accepted with a pay link
    Notification.objects.create(
        user=offer.buyer,
        message=f"Your offer of €{offer.amount} on '{sale.title}' has been accepted!"
        f"Click <a href='{reverse('pay_offer', args=[offer.id])}'>here</a> to pay now.",
    )
    return redirect("profile")


@login_required
def reject_offer(request, offer_id):
    """Reject an offer on a sale item listing by a user (buyer) on a sale item"""
    offer = get_object_or_404(Offer, id=offer_id, sale__user=request.user)
    if offer.status != "pending":
        return redirect("profile")
    # Add logic to handle rejection
    offer.status = "rejected"
    offer.save()
    # Notify buyer that their offer was rejected
    Notification.objects.create(
        user=offer.buyer,
        message=f"Your offer of €{offer.amount} on '{offer.sale.title}' has been rejected.",
    )
    return redirect("profile")


@login_required
def pay_offer(request, offer_id):
    """Allow buyer to pay for an accepted offer using Stripe"""
    offer = get_object_or_404(Offer, id=offer_id, buyer=request.user, status="accepted")
    sale = offer.sale
    if sale.status != "pending":
        return redirect("profile")
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "eur",
                    "product_data": {"name": sale.title},
                    "unit_amount": int(offer.amount * 100),  # Use original offer amount
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=request.build_absolute_uri("/sales/payment_result/")
        + f"?session_id={{CHECKOUT_SESSION_ID}}&offer_id={offer.id}",
        cancel_url=request.build_absolute_uri("/sales/payment_result/")
        + f"?offer_id={offer.id}",
        metadata={"offer_id": offer.id, "sale_id": sale.id},
    )
    return redirect(session.url, code=303)


# Counter offer view for buyers and sellers to make and accept/reject counter offers on sale items
@login_required
def counter_offer(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id, sale__user=request.user)
    if offer.status != "pending":
        return redirect("profile")

    if request.method == "POST":
        counter_amount = request.POST.get("counter_amount")
        try:
            counter_amount = float(counter_amount)
            if counter_amount <= 0:
                raise ValueError
            offer.counter_amount = counter_amount
            offer.counter_status = "pending"
            offer.save()
            # Notify the buyer with corrected message
            profile_url = reverse("profile")
            message = f"The seller countered your offer of €{offer.amount} on"
            f"'{offer.sale.title}' with €{counter_amount}."
            Notification.objects.create(
                user=offer.buyer,
                message=message,
            )
            return redirect("profile")
        except ValueError:
            return render(
                request,
                "sales/counter_offer.html",
                {"offer": offer, "error": "Invalid amount"},
            )
    return render(request, "sales/counter_offer.html", {"offer": offer})


@login_required
def respond_counter_offer(request, offer_id):
    """Respond to a counter offer on a sale item listing by a user (buyer) on a sale item"""
    offer = get_object_or_404(Offer, id=offer_id, buyer=request.user)
    if offer.counter_status != "pending":
        return redirect("profile")
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "accept":
            offer.counter_status = "accepted"
            offer.status = "accepted"  # Original offer accepted too
            offer.save()
            sale = offer.sale
            sale.status = "sold"
            sale.save()
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "eur",
                            "product_data": {"name": offer.sale.title},
                            "unit_amount": int(offer.counter_amount * 100),
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url=request.build_absolute_uri("/sales/offer_success/")
                + f"?session_id={{CHECKOUT_SESSION_ID}}&offer_id={offer.id}",
                cancel_url=request.build_absolute_uri("/sales/offer_cancel/")
                + f"?offer_id={offer.id}",
                metadata={"offer_id": offer.id, "sale_id": sale.id},
            )
            return redirect(session.url, code=303)
        elif action == "reject":
            offer.counter_status = "rejected"
            offer.save()
            Notification.objects.create(
                user=offer.sale.user,
                message=f"Buyer rejected your counteroffer of"
                f" €{offer.counter_amount} on '{offer.sale.title}'.",
            )
            return redirect("profile")
    return render(request, "sales/respond_counter_offer.html", {"offer": offer})


def offer_payment_success(request):
    session_id = request.GET.get("session_id")
    offer_id = request.GET.get("offer_id")

    if not session_id or not offer_id:
        messages.error(request, "Invalid payment session.")
        return redirect("profile")

    try:
        session = stripe.checkout.Session.retrieve(session_id)
        if session.payment_status != "paid":
            messages.error(request, "Payment was not successful.")
            return redirect("profile")
    except stripe.error.StripeError as e:
        messages.error(request, "Error verifying payment. Please contact support.")
        return redirect("profile")

    offer = get_object_or_404(Offer, id=offer_id, buyer=request.user)
    if offer.status != "accepted":
        messages.error(request, "Offer is not in a valid state for payment.")
        return redirect("profile")

    sale = offer.sale
    sale.status = "sold"
    sale.save()

    # Update the offer and create Purchase with price_paid
    offer.status = "paid"
    offer.save()
    purchase = Purchase.objects.create(
        buyer=request.user,
        sale=sale,
        price_paid=offer.amount,  # Use the offer amount as the price paid
    )

    # Notify the seller
    Notification.objects.create(
        user=sale.user,
        message=f"Your item '{sale.title}' has been sold for €{offer.amount} to {request.user.username}.",
    )

    messages.success(
        request,
        f"Payment successful! You have purchased '{sale.title}' for €{offer.amount}.",
    )
    return render(
        request, "sales/offer_payment_success.html", {"offer": offer, "sale": sale}
    )


# Add this view function at the end of the file
def payment_result(request):
    """Handle the redirect from Stripe after payment"""
    session_id = request.GET.get("session_id")
    offer_id = request.GET.get("offer_id")

    if not session_id or not offer_id:
        messages.error(request, "Invalid payment session.")
        return redirect("profile")

    try:
        # Verify the payment was successful
        session = stripe.checkout.Session.retrieve(session_id)

        if session.payment_status == "paid":
            # Get the offer and mark it as paid
            offer = get_object_or_404(Offer, id=offer_id)
            offer.status = "paid"
            offer.save()

            # Update the sale status
            sale = offer.sale
            sale.status = "sold"
            sale.save()

            # Create a purchase record
            Purchase.objects.create(
                buyer=request.user,
                sale=sale,
                price_paid=offer.amount,  # Use the offer amount
            )

            # Notify the seller
            Notification.objects.create(
                user=sale.user,
                message=f"Your item '{sale.title}' has been sold for €{offer.amount} to {request.user.username}.",
            )

            messages.success(
                request, "Payment successful! The seller has been notified."
            )
            return render(
                request,
                "sales/payment_result.html",
                {"success": True, "sale": sale, "price": offer.amount},
            )
        else:
            messages.error(request, "Payment not completed. Please try again.")
            return render(request, "sales/payment_result.html", {"success": False})
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return render(request, "sales/payment_result.html", {"success": False})


def offer_payment_cancel(request):
    """Payment cancel view for accepting an offer"""
    offer_id = request.GET.get("offer_id")
    sale = None
    if offer_id:
        try:
            offer = get_object_or_404(Offer, id=offer_id)
            sale = offer.sale  # Get the sale associated with the offer
        except Offer.DoesNotExist:
            pass  # Fallback to None if offer doesn’t exist
    return render(
        request, "sales/payment_result.html", {"success": False, "sale": sale}
    )
