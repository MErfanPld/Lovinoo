from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from activity.models import ReportedUser
from chat.models import Message, Room
from financial.models import CartPay, OriginCart, PayHistory, Tariff
from utils.mixins import AdminUserMixin

# from .forms import AboutUsForm, RuleForm
from .models import Contact
# from .models import AboutUs, Contact, Rules

user = get_user_model()


def home(request):
    return render(request, "index.html")


class PanelView(AdminUserMixin, View):
    def get(self, request, *args, **kwargs):
        user_count = user.objects.exclude(is_admin=True, is_superuser=True).count()
        admin_count = user.objects.filter(is_admin=True).count()
        tariff_count = Tariff.objects.count()
        origin_cart_count = OriginCart.objects.count()
        pay_count = PayHistory.objects.count()
        cart_pay_count = CartPay.objects.filter(status="waiting").count()
        reported_count = ReportedUser.objects.all().count()
        contact_count = Contact.objects.count()
        total_pay = PayHistory.objects.aggregate(total_pay=Sum("price"))["total_pay"]
        message_count = Message.objects.count()
        room_count = Room.objects.count()
        context = {
            "user_count": user_count,
            "admin_count": admin_count,
            "total_pay": total_pay,
            "tariff_count": tariff_count,
            "origin_cart_count": origin_cart_count,
            "pay_count": pay_count,
            "cart_pay_count": cart_pay_count,
            "reported_count": reported_count,
            "contact_count": contact_count,
            "message_count": message_count,
            "room_count": room_count,
        }
        return render(request, "config/home.html", context)


class AboutUsView(View):
    def get(self, request):
        about_us = AboutUs.load()
        return render(request, "config/about_us.html", {"about_us": about_us})


class RuleView(View):
    def get(self, request):
        about_us = Rules.load()
        return render(request, "config/rule.html", {"rule": about_us})


class ContactListView(ListView):
    model = Contact
    template_name = "config/contact_list.html"


class ContactDetailView(DetailView):
    model = Contact
    template_name = "config/contact_detail.html"


class AboutUsCreateView(CreateView):
    model = AboutUs
    form_class = AboutUsForm
    template_name = "config/about_create.html"
    success_url = reverse_lazy("config:about_us")


class RuleCreateView(CreateView):
    model = Rules
    form_class = RuleForm
    template_name = "config/rule_create.html"
    success_url = reverse_lazy("config:rule")


class StaticView(AdminUserMixin, View):
    def get(self, request, *args, **kwargs):
        # category = Category.objects.all()
        # want_ad = WantAd.objects.all()
        # today_want_ad = want_ad.filter(created=jdatetime.date.today())
        # not_confirmed = today_want_ad.filter(confirmed=False).count()
        # month_want_ad = want_ad.filter(created__month=jdatetime.date.today().month).count()
        # year_want_ad = want_ad.filter(created__year=jdatetime.date.today().year).count()
        # special_want = want_ad.filter(express=True).count()
        # top_city = want_ad.annotate(top_city=Count('city')).order_by('-top_city').first()
        # top_date = want_ad.annotate(top_date=Count('created')).order_by('-created').first()
        # top_zone = want_ad.annotate(top_zone=Count('zone')).order_by('-top_zone').first()
        # paid = want_ad.filter(category__paid=True).count()
        # parent_category = category.filter(parent=None).count()
        # child_category = category.count() - parent_category
        # context = {
        #     'today_want_ad': today_want_ad.count(),
        #     'month_want_ad': month_want_ad,
        #     'year_want_ad': year_want_ad,
        #     'special': special_want,
        #     'top_city': top_city,
        #     'top_zone': top_zone,
        #     'paid': paid,
        #     'not_confirmed': not_confirmed,
        #     'category_count': category.count(),
        #     'parent_category': parent_category,
        #     'child_category': child_category,
        #     'top_date': top_date,
        # }
        return render(request, "config/static.html")


class LandingView(TemplateView):
    template_name = "config/landing.html"
