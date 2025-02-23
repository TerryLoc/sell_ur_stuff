from django import forms
from .models import Sale, Offer


class SaleForm(forms.ModelForm):
    """
    Form for creating and updating sale listings
    """

    class Meta:
        model = Sale
        fields = [
            "title",
            "description",
            "price",
            "image",
            "image_1",
            "image_2",
            "image_3",
            "video",
        ]  # fields to be displayed in the form


class OfferForm(forms.ModelForm):
    """
    Form for creating an offer on a sale item listing by a user (buyer) on a sale item
    """

    def __init__(self, *args, **kwargs):
        # Still need sale for validation, but we won’t touch the widget
        self.sale = kwargs.pop("sale", None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Offer
        fields = ["amount"]
        widgets = {
            "amount": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "min": "0.01",  # Keep this as a basic positive check
                    "placeholder": "Enter your offer in euros",
                }
            )
        }

    def clean_amount(self):
        """Custom validation for the amount field so that it is at least 50% of the asking price"""
        amount = self.cleaned_data["amount"]
        if self.sale and amount < self.sale.price * 0.5:
            raise forms.ValidationError(
                f"Offer must be at least €{self.sale.price * 0.5:.2f} (50% of asking price)."
            )
        return amount
