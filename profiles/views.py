from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Purchase, Notification
from sales.models import Sale
from .forms import UserProfileForm  # We’ll create this


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
