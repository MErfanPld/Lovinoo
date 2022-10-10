from django.views.generic import ListView

from utils.mixins import AdminUserMixin

from .models import ReportedUser


# Create your views here.
class ReportedUserList(AdminUserMixin, ListView):
    model = ReportedUser
    template_name = "activity/reported_list.html"
