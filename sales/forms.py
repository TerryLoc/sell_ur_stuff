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
            "image_2",
            "image_3",
            "video",
        ]  # fields to be displayed in the form
