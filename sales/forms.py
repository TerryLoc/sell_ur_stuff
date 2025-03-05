from django import forms
from .models import Sale, Offer
from decimal import Decimal  # Import Decimal for currency handling


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
    Form for making an offer on a sale listing with a custom amount field
    """

    def __init__(self, *args, sale=None, **kwargs):
        super(OfferForm, self).__init__(*args, **kwargs)
        if sale:
            placeholder_text = f"€{sale.price}"
            self.fields["amount"].widget = forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "min": "0.01",
                    "placeholder": placeholder_text,
                }
            )

    class Meta:
        model = Offer
        fields = ["amount"]

    def clean_amount(self):
        """
        Ensure that the offer is at least 50% of the asking price of the sale
        """
        amount = self.cleaned_data["amount"]
        if self.sale and amount < self.sale.price * Decimal(
            "0.5"
        ):  # Convert 0.5 to Decimal
            min_amount = self.sale.price * Decimal("0.5")
            raise forms.ValidationError(
                f"Offer must be at least €{min_amount:.2f} (50% of asking price)."
            )
        return amount
