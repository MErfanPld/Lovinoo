from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, View

from .forms import OriginCartForm, TariffForm
from .models import CartPay, OriginCart, PayHistory, Tariff

# Create your views here.


class TariffCreateView(SuccessMessageMixin, CreateView):
    model = Tariff
    form_class = TariffForm
    success_url = reverse_lazy("financial:tariff_list")
    success_message = ""
    template_name = "financial/tariff_create.html"

    def form_invalid(self, form):
        messages.error(self.request, "", "")
        return super(TariffCreateView, self).form_invalid(form)


class TariffListView(ListView):
    model = Tariff
    template_name = "financial/tariff_list.html"


class TariffUpdateView(SuccessMessageMixin, UpdateView):
    model = Tariff
    form_class = TariffForm
    success_url = reverse_lazy("financial:tariff_list")
    success_message = "پلن با موفقیت به روززسانی شد"
    template_name = "financial/tariff_update.html"

    def form_invalid(self, form):
        messages.error(self.request, "حطا", "danger")
        return super(TariffUpdateView, self).form_invalid(form)


class TariffDeleteView(View):
    def get(self, request, pk):
        tariff = get_object_or_404(Tariff, pk=pk)
        tariff.delete()
        messages.success(request, "پلن با موفقیت حذف شد", "success")
        return redirect("financial:tariff_list")


class OriginCartListView(ListView):
    model = OriginCart
    template_name = "financial/origin_list.html"


class OriginCartCreateView(SuccessMessageMixin, CreateView):
    model = OriginCart
    form_class = OriginCartForm
    success_url = reverse_lazy("financial:origin_list")
    success_message = ""
    template_name = "financial/origin_create.html"

    def form_invalid(self, form):
        messages.error(self.request, "", "")
        return super(OriginCartCreateView, self).form_invalid(form)


class OriginUpdateView(SuccessMessageMixin, UpdateView):
    model = OriginCart
    form_class = OriginCartForm
    success_url = reverse_lazy("financial:origin_list")
    success_message = "پلن با موفقیت به روززسانی شد"
    template_name = "financial/tariff_update.html"

    def form_invalid(self, form):
        messages.error(self.request, "حطا", "danger")
        return super(OriginUpdateView, self).form_invalid(form)


class OriginDeleteView(View):
    def get(self, request, pk):
        origin_cart = get_object_or_404(OriginCart, pk=pk)
        origin_cart.delete()
        messages.success(request, "پلن با موفقیت حذف شد", "success")
        return redirect("financial:origin_list")


class CartPayAcceptedListView(ListView):
    queryset = CartPay.objects.filter(status="accepted")
    template_name = "financial/cartpay_list.html"


class CartPayNotConfirmedListView(ListView):
    queryset = CartPay.objects.filter(status="waiting")
    template_name = "financial/cart_pay_wait.html"


class PayHistoryListView(ListView):
    model = PayHistory
    template_name = "financial/pay_list.html"
