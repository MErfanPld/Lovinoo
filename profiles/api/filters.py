from django_filters import rest_framework as filters

from ..models import Profile


class ProfileFilter(filters.FilterSet):
    # min_age = filters.NumberFilter(field_name="age", lookup_expr='gte')
    # max_age = filters.NumberFilter(field_name="age", lookup_expr='lte')

    class Meta:
        model = Profile
        fields = [
            "province",
            "city",
            "status",
        ]


#
# class ProfileFilterSet(PropertyFilterSet):
#
#   class Meta:
#       model = Profile
#       fields = ['province','city','status']
#       property_fields = [
#         ('age', PropertyNumberFilter, ['lt', 'exact']),
#         ('has_image', PropertyBooleanFilter),
#       ]
