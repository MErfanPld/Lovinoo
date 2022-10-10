from django import forms

from .models import OriginCart, Tariff


class TariffForm(forms.ModelForm):
    class Meta:
        model = Tariff
        fields = (
            "title",
            "price",
            "time",
        )
        labels = {
            "title": "عنوان اشتراک",
            "price": "قیمت اشتراک ",
            "time": "مدت اشتراک",
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "time": forms.NumberInput(attrs={"class": "form-control"}),
        }


class OriginCartForm(forms.ModelForm):
    class Meta:
        model = OriginCart
        fields = ("number",)
        labels = {
            "number": "شماره کارت",
        }
        widgets = {
            "number": forms.TextInput(attrs={"class": "form-control"}),
        }
