from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Purchase, Notification
from sales.models import Sale


@login_required
def profile_view(request):
    profile = request.user.profile
    sales = Sale.objects.filter(user=request.user)  # Products user is selling
    purchases = Purchase.objects.filter(buyer=request.user)  # Products user bought
    notifications = Notification.objects.filter(user=request.user, is_read=False)

    return render(
        request,
        "profiles/profile.html",
        {
            "profile": profile,
            "sales": sales,
            "purchases": purchases,
            "notifications": notifications,
        },
    )
