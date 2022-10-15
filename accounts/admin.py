from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from profiles.models import Image, Profile

from .forms import UserChangeForm, UserCreationForm
from .models import OtpCode, User

admin.site.register(OtpCode)


# Register your models here.
class ProfileAdminInline(admin.StackedInline):
    model = Profile


class ImageAdminInline(admin.StackedInline):
    model = Image
    extra = 1


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    inlines = [ProfileAdminInline, ImageAdminInline]

    list_display = ("phone_number",)
    list_filter = (
        "is_admin",
        "is_active",
    )
    search_fields = ("phone_number",)
    readonly_fields = ("last_login",)
    ordering = ("phone_number",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

    fieldsets = (
        (
            "Main",
            {"fields": ("phone_number","fcm_token")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_admin",
                    "is_superuser",
                    "last_login",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "phone_number",
                    "password",
                    "password_confirm",
                )
            },
        ),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            form.base_fields["is_superuser"].disabled = True
        return form
