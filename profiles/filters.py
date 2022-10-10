import django_filters as filters
from django.db.models import Q, Value
from django.db.models.functions import Concat

class ProfileFilters(filters.FilterSet):
    search = filters.CharFilter(method="search_filter")
    status = filters.CharFilter(method="status_filter")
    province = filters.CharFilter(method="province_filter")
    city = filters.CharFilter(method="city_filter")
    confirmed_image = filters.CharFilter(method="confirmed_image_filter")
    age_gt = filters.CharFilter(method="age_gt_filter")
    age_lt = filters.CharFilter(method="age_lt_filter")

    @staticmethod
    def search_filter(qs, name, value):
        qs = qs.filter(
            Q(user__phone_number__icontains=value) |
            Q(first_name__icontains=value) |
            Q(last_name__icontains=value) |
            Q(bio__icontains=value) |
            Q(user_name__icontains=value)
        ).distinct()
        return qs

    @staticmethod
    def status_filter(qs, name, value):
        qs = qs.filter(status=value)
        return qs

    @staticmethod
    def province_filter(qs, name, value):
        qs = qs.filter(province=value)
        return qs

    @staticmethod
    def city_filter(qs, name, value):
        qs = qs.filter(city=value)
        return qs

    @staticmethod
    def confirmed_image_filter(qs, name, value):
        qs = qs.filter(confirmed_image=value)
        return qs

    @staticmethod
    def age_gt_filter(qs, name, value):
        qs = qs.filter(age__gte=value)
        return qs

    @staticmethod
    def age_lt_filter(qs, name, value):
        qs = qs.filter(age__lte=value)
        return qs


