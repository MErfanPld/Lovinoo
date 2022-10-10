from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, UpdateView, View

from utils.mixins import AdminUserMixin

from .models import Profile

user=get_user_model()

# Create your views here.
class ProfileListView(AdminUserMixin, ListView):
    model = Profile
    template_name = ''


class ProfileDetailView(DetailView):
    model = Profile
    template_name = ''
    slug_field = 'user_name'
    slug_url_kwarg = 'user_name'


class ProfileUpdateView(AdminUserMixin, UpdateView):
    model = Profile
    success_url = reverse_lazy()
    template_name = ''
    form_class =

    def form_valid(self, form):
        messages.success()
        return super(ProfileUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error()
        return super(ProfileUpdateView, self).form_invalid(form)

class ProfileDeleteView(AdminUserMixin,View):
    def get(self,request,user_name):
        user_obj=user.objects.filter(profile__user_nmae__iexact=user_name)
        user_obj.delete()
        return redirect('')
