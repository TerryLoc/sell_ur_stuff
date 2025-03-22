from django import forms
from .models import NewsletterSubscriber


class NewsletterSubscriptionForm(forms.ModelForm):
    """Form to subscribe to the newsletter"""

    class Meta:
        model = NewsletterSubscriber
        fields = ["email"]
        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control custom-input",
                    "placeholder": "Enter your email",
                    "required": "required",
                }
            ),
        }

    def clean_email(self):
        """Check if the email is already subscribed"""
        email = self.cleaned_data.get("email")
        if NewsletterSubscriber.objects.filter(email=email, is_active=True).exists():
            raise forms.ValidationError("This email is already subscribed.")
        return email
