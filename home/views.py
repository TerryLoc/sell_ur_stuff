from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import NewsletterSubscriptionForm
from django.urls import reverse


def home_view(request):
    """View function for the home page with newsletter subscription form"""
    if request.method == "POST":
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for subscribing to our newsletter!")
            # Redirect with fragment to maintain position
            return redirect(reverse("home") + "#newsletter")
    else:
        form = NewsletterSubscriptionForm()

    return render(request, "home/home.html", {"form": form})
