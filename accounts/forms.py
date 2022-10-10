from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.validators import ValidationError

from .models import User


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("phone_number",)

    # def clean(self):
    #     cleand_data = super(UserCreationForm, self).clean()
    #     password = cleand_data["password"]
    #     password_confirm = cleand_data["password_confirm"]
    #     if (password and password_confirm) and (password_confirm != password_confirm):
    #         raise ValidationError("unmatched password")
    #     return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text='you can change password using <a href="../password/">this form</a>.'
    )

    class Meta:
        model = User
        fields = (
            "phone_number",
            "password",
        )


class AuthForm(forms.Form):
    phone_number = forms.CharField(
        label="نام کاربری",
        widget=forms.TextInput(
            attrs={"placeholder": "نام کاربری", "class": "form-control text-left"}
        ),
    )

    password = forms.CharField(
        label="رمز عبوز",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "رمز عبور",
                "class": "form-control text-left",
            }
        ),
    )


class AdminForm(AuthForm):
    password_confirm = forms.CharField(
        label="نایید رمز عبور",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "تایید  رمز عبوز",
                "class": "form-control text-left",
            }
        ),
    )

    def clean(self):
        clean_data = super(AdminForm, self).clean()
        password, password_confirm = (
            clean_data["password"],
            clean_data["password_confirm"],
        )
        if (password and password_confirm) and (password != password_confirm):
            raise ValidationError("dis match")
