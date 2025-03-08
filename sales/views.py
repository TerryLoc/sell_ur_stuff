import stripe
import json
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from profiles.models import Purchase, Notification
from .models import Sale, Offer
from .forms import SaleForm, OfferForm

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
    View details of a single sale listing with the option to buy the product
    """
    sale = get_object_or_404(Sale, id=sale_id)
    purchase = None
    if sale.status == "sold" and request.user.is_authenticated:
        purchase = Purchase.objects.filter(sale=sale, buyer=request.user).first()
    return render(
        request, "sales/sale_detail.html", {"sale": sale, "purchase": purchase}
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
            return JsonResponse(
                # Return a JSON response with a success message if the form is valid
                {
                    "status": "success",
                    "message": f"Sale of'{sale.title}' created successfully!",
                }
            )
        else:
            return JsonResponse(
                # Return a JSON response with an error message if the form is invalid
                {
                    "status": "error",
                    "message": "Failed to create the sale. Please check the form and images.",
                },
                status=400,
            )
    else:
        form = SaleForm()
    return render(request, "sales/sale_form.html", {"form": form})


# Update an existing sale
@login_required
def sale_update(request, sale_id):
    """
    Update an existing sale listing ie. change the details of a sale listing
    """
    sale = get_object_or_404(Sale, id=sale_id, user=request.user)
    if sale.status == "sold":
        return redirect("sales_list")  # Or render an error page
    if request.method == "POST":
        form = SaleForm(request.POST, request.FILES, instance=sale)
        if form.is_valid():
            form.save()
            return JsonResponse(
                # Return a JSON response with a successful update message
                {
                    "status": "success",
                    "message": f"Sale '{sale.title}' updated successfully!",
                }
            )
        else:
            return JsonResponse(
                # Return a JSON response with an error message if update fails
                {
                    "status": "error",
                    "message": "Failed to update sale. Please check the form.",
                },
                status=400,
            )
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
        return JsonResponse(
            # JSON response with a warning message if the sale is sold
            {"status": "warning", "message": "Cannot delete a sold item."},
            status=400,
        )
    if request.method == "POST":
        sale_title = sale.title
        sale.delete()
        return JsonResponse(
            # JSON response with a success message if the sale item is deleted
            {
                "status": "success",
                "message": f"Sale '{sale_title}' is deleted successfully!",
            }
        )
    return render(request, "sales/sale_confirm_delete.html", {"sale": sale})


# Buy a product
@login_required
def buy_product(request, sale_id):
    """
    Buy a product using the Stripe API and redirect to the payment page on Stripe
    """
    sale = get_object_or_404(Sale, id=sale_id)
    if sale.status != "available":
        return JsonResponse(
            # JSON response with a warning message if the sale is not available
            {"status": "warning", "message": "This item is no longer available."},
            status=400,
        )
    session = stripe.checkout.Session.create(
        # Create a Stripe session for the sale item with the user's details
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
    return JsonResponse(
        # JSON response with a success message and the Stripe session
        {
            "status": "info",
            "message": f"Proceeding to payment section for '{sale.title}'...",
            "redirect": session.url,
        }
    )


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
        )
        return render(
            # Render the payment result page with a success message if payment is successful
            request,
            "sales/payment_result.html",
            {
                "success": True,
                "sale": sale,
                "message": f"Payment successful! Congrats... you bought '{sale.title}' for €{sale.price}.",
                "message_type": "success",
            },
        )

    return render(
        # Render the payment result page with a failure message if payment fails
        request,
        "sales/payment_result.html",
        {
            "success": False,
            "sale": sale,
            "message": "Payment failed. Please try again.",
            "message_type": "error",
        },
    )


def payment_cancel(request):
    """
    Payment cancel view that redirects to the payment result page with a failure message
    """
    return render(
        # Render the payment result page with a cancellation message if payment is cancelled
        request,
        "sales/payment_result.html",
        {"success": False, "message": "Payment cancelled.", "message_type": "info"},
    )


# Offer views for buyers and sellers to make and accept/reject offers on sale items. Also, counter offers are included.
@login_required
def make_offer(request, sale_id):
    """
    Make an offer on a sale item listing by a user (buyer) on a sale item
    """
    sale = get_object_or_404(Sale, id=sale_id)
    if sale.status != "available":
        return JsonResponse(
            # JSON warning message if the item is not available
            {"status": "warning", "message": "This item is no longer available."},
            status=400,
        )
    if request.method == "POST":
        form = OfferForm(request.POST, sale=sale)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.sale = sale
            offer.buyer = request.user
            offer.save()
            Notification.objects.create(
                # Notify the seller of the offer made on their item
                user=sale.user,
                message=f"You have a new offer of €{offer.amount} on your item '{sale.title}' from {request.user.username}!",
            )
            return JsonResponse(
                # JSON success message if the offer is successfully submitted
                {
                    "status": "success",
                    "message": f"Your offer of €{offer.amount} was submitted for '{sale.title}'!",
                }
            )
        else:
            return JsonResponse(
                # JSON error message if the offer submission fails
                {
                    "status": "error",
                    "message": "You failed to submit an offer. Please check your input.",
                },
                status=400,
            )
    else:
        form = OfferForm(sale=sale)
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

    Notification.objects.create(
        # Notify the buyer that their offer was accepted with a payment link
        user=offer.buyer,
        message=f"Your offer of €{offer.amount} on '{sale.title}' has been accepted! Click <a href='{reverse('pay_offer', args=[offer.id])}'>here</a> to pay now.",
    )
    return JsonResponse(
        # JSON success message if the offer is accepted
        {
            "status": "success",
            "message": f"Offer of €{offer.amount} on '{sale.title}' accepted. WOOOO!",
        }
    )


@login_required
def reject_offer(request, offer_id):
    """Reject an offer on a sale item listing by a user (buyer) on a sale item"""
    offer = get_object_or_404(Offer, id=offer_id, sale__user=request.user)
    if offer.status != "pending":
        return redirect("profile")
    # Add logic to handle rejection
    offer.status = "rejected"
    offer.save()

    Notification.objects.create(
        # Notify buyer that their offer was rejected
        user=offer.buyer,
        message=f"Your offer of €{offer.amount} on '{offer.sale.title}' has been rejected.",
    )
    return JsonResponse(
        # JSON message that the offer is rejected
        {
            "status": "success",
            "message": f"The offer of €{offer.amount} on '{offer.sale.title}' was rejected.",
        }
    )


@login_required
def pay_offer(request, offer_id):
    """Allow buyer to pay for an accepted offer using Stripe API and redirect to the payment page"""
    offer = get_object_or_404(Offer, id=offer_id, buyer=request.user, status="accepted")
    sale = offer.sale
    if sale.status != "pending":
        return redirect("profile")
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    # Use the original amount for the sale item
                    "currency": "eur",
                    "product_data": {"name": sale.title},
                    "unit_amount": int(offer.amount * 100),  # Original amount
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=request.build_absolute_uri("/sales/offer_payment_success/")
        + f"?session_id={{CHECKOUT_SESSION_ID}}&offer_id={offer.id}",
        cancel_url=request.build_absolute_uri("/sales/offer_payment_cancel/")
        + f"?offer_id={offer.id}",
        metadata={"offer_id": offer.id, "sale_id": sale.id},
    )
    return JsonResponse(
        # JSON message to proceed to payment of the accepted offer
        {
            "status": "info",
            "message": f"Proceeding to payment for '{sale.title}'...",
            "redirect": session.url,
        }
    )


# Counter offer view for buyers and sellers to make and accept/reject counter offers on sale items
@login_required
def counter_offer(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id, sale__user=request.user)
    if offer.status != "pending":
        return JsonResponse(
            # JSON warning message if the offer is not pending
            {"status": "warning", "message": "You cannot counter this offer."},
            status=400,
        )
    if request.method == "POST":
        counter_amount = request.POST.get("counter_amount")
        try:
            counter_amount = float(counter_amount)
            if counter_amount <= 0:
                raise ValueError
            offer.counter_amount = counter_amount
            offer.counter_status = "pending"
            offer.save()
            Notification.objects.create(
                user=offer.buyer,
                message=f"Seller countered your offer of €{offer.amount} on '{offer.sale.title}' with €{counter_amount}.",
            )
            return JsonResponse(
                # JSON success message if the counter offer is submitted
                {
                    "status": "success",
                    "message": f"Your counter offer of €{counter_amount} has been submitted for '{offer.sale.title}'! Best of Luck!",
                }
            )
        except ValueError:
            return JsonResponse(
                # JSON error message if the counter offer is invalid
                {"status": "error", "message": "Invalid counteroffer amount."},
                status=400,
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
                message=f"Buyer rejected your counteroffer of €{offer.counter_amount} on '{offer.sale.title}'.",
            )
            return redirect("profile")
    return render(request, "sales/respond_counter_offer.html", {"offer": offer})


def offer_payment_success(request):
    """Payment success view for accepting an offer and completing the sale"""
    session_id = request.GET.get("session_id")
    offer_id = request.GET.get("offer_id")
    session = stripe.checkout.Session.retrieve(session_id)
    offer = get_object_or_404(Offer, id=offer_id)
    if session.payment_status == "paid":
        sale = offer.sale
        sale.status = "sold"  # Update to sold after payment
        sale.save()
        # Determine the final price: counter_amount if accepted, otherwise amount
        price = (
            offer.counter_amount
            if offer.counter_amount and offer.counter_status == "accepted"
            else offer.amount
        )
        Purchase.objects.create(
            buyer=offer.buyer,
            sale=sale,
            price_paid=price,  # Set to final offer or counteroffer price
        )  # Triggers notification
        offer.status = "accepted"
        offer.save()
        return render(
            request,
            "sales/payment_result.html",
            {"success": True, "sale": sale, "price": price},
        )
    return render(
        request, "sales/payment_result.html", {"success": False, "sale": offer.sale}
    )


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
