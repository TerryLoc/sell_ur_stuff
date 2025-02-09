from django import forms
from .models import Sale


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
            "video",
        ]  # Include video field
