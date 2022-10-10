from braces.views import (AnonymousRequiredMixin, LoginRequiredMixin,
                          SuperuserRequiredMixin)
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

from django.views.generic import DetailView, FormView, ListView, View

from .forms import AdminForm, AuthForm

user = get_user_model()


class AdminLoginView(AnonymousRequiredMixin, View):
    """
    login view for accessing panel
    """

    form_class = AuthForm
    template_name = "accounts/login.html"

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user_obj = authenticate(
                phone_number=cd["phone_number"], password=cd["password"]
            )
            if user_obj and user_obj.is_admin:
                login(request, user_obj)
                messages.success(request, "با موفقیت وارد شدید", "success")
                return redirect("config:panel")
            messages.error(request, "خطا در ورود", "danger")
        return render(request, self.template_name, {"form": form})


class AddNewAdminView(SuccessMessageMixin, FormView):
    form_class = AdminForm
    success_url = reverse_lazy("accounts:admin_list")
    template_name = "accounts/admin_create.html"
    success_message = "ادمین با موققیت اضافه شد"

    def form_valid(self, form):
        clean_data = form.cleaned_data
        user(phone_number=clean_data["phone_number"],
             password=clean_data["password"])
        user.is_admin = True
        user.save()
        return super(AddNewAdminView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "خطا در افزودن کاربر ادمین", "danger")
        return super(AddNewAdminView, self).form_invalid(form)


class UserDeleteView(SuperuserRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        user_obj = get_object_or_404(user, id=user_id)
        user_obj.delete()
        messages.success(
            request, "کاربر با موفقیت حذف شد و ابن شماره به لیست کاربران بلاک شده انتقال پیدا کرد", "success")
        return redirect(request.META.get('HTTP_REFERER'))


class AdminListView(ListView):
    def get_queryset(self):
        admin_list = user.objects.filter(is_admin=True, is_superuser=False)
        return admin_list

    template_name = "accounts/admin_list.html"


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, "", "success")
        return redirect("accounts:login")


class UserListView(ListView):
    queryset = user.objects.exclude(
        is_admin=True, is_superuser=True).select_related('profile')
    template_name = "accounts/user_list.html"


class UserDetailView(DetailView):
    queryset = user.objects.exclude(
        is_admin=True, is_superuser=True).select_related('profile')
    template_name = "accounts/user_detail.html"
    context_object_name = 'user'
