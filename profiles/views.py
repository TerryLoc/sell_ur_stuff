from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Purchase, Notification, Sale, Offer
from .forms import UserProfileForm


@login_required
def profile_view(request):
    """
    View the user's profile page for the logged-in user with their sales, purchases, offers, and notifications.
    """
    profile = request.user.profile
    active_sales = Sale.objects.filter(user=request.user, status="available")
    # Get sold items with purchase details
    sold_sales = Purchase.objects.filter(sale__user=request.user).select_related(
        "sale", "buyer"
    )
    # Get purchases with sale and seller details
    purchases = Purchase.objects.filter(buyer=request.user).select_related("sale__user")
    # Get offers received on user's sales
    offers = (
        Offer.objects.filter(sale__user=request.user)
        .order_by("-created_at")
        .select_related("sale", "buyer")
    )
    # Notifications handling
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    if notifications.exists():
        notifications.update(is_read=True)
    all_notifications = Notification.objects.filter(user=request.user)

    return render(
        request,
        "profiles/profile.html",
        {
            "profile": profile,
            "active_sales": active_sales,
            "sold_sales": sold_sales,
            "purchases": purchases,
            "offers": offers,  # Added offers context
            "notifications": notifications,
            "all_notifications": all_notifications,
        },
    )


@login_required
def profile_edit(request):
    profile = request.user.profile
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = UserProfileForm(instance=profile)
    return render(request, "profiles/profile_form.html", {"form": form})
