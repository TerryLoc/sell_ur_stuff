from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from profiles.models import UserProfile, Purchase, Notification
from sales.models import Sale, Offer
from .forms import UserProfileForm


@login_required
def profile_view(request):
    profile = request.user.profile
    active_sales = Sale.objects.filter(user=request.user, status="available")
    sold_sales = Purchase.objects.filter(sale__user=request.user).select_related(
        "sale", "buyer"
    )
    purchases = Purchase.objects.filter(buyer=request.user).select_related("sale__user")
    offers = Offer.objects.filter(sale__user=request.user).order_by(
        "-created_at"
    )  # Offers as seller
    offers_made = Offer.objects.filter(buyer=request.user).order_by(
        "-created_at"
    )  # Offers as buyer
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
            "offers": offers,
            "offers_made": offers_made,
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
