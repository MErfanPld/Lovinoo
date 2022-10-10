from django import forms

from .models import AboutUs, Rules


class AboutUsForm(forms.ModelForm):
    class Meta:
        model = AboutUs
        fields = {
            "title",
            "description",
        }
        labels = {
            "title": "عنوان",
            "description": "توضیحات",
        }
        widgets = {"title": forms.TextInput(attrs={"class": "form-control"})}


class RuleForm(forms.ModelForm):
    class Meta:
        model = Rules
        fields = {
            "title",
            "description",
        }
        labels = {
            "title": "عنوان",
            "description": "توضیحات",
        }
        widgets = {"title": forms.TextInput(attrs={"class": "form-control"})}
