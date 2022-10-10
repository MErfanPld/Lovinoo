from django.utils.safestring import mark_safe
from rest_framework import serializers

from ..models import Contact,Rate


# class AboutUsSerializer(serializers.ModelSerializer):
#     description = serializers.SerializerMethodField()

#     class Meta:
#         model = AboutUs
#         fields = (
#             "title",
#             "description",
#         )

#     def get_description(self, obj):
#         return mark_safe(obj.description)


# class RulesSerializer(serializers.ModelSerializer):
#     description = serializers.SerializerMethodField()

#     class Meta:
#         model = Rules
#         fields = (
#             "title",
#             "description",
#         )

#     def get_description(self, obj):
#         return mark_safe(obj.description)


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = (
            "title",
            "email",
            "description",
            "created",
        )
        read_only_fields = ("created",)



# class PrivacySerializer(serializers.ModelSerializer):
#     description = serializers.SerializerMethodField()

#     class Meta:
#         model = Privacy
#         fields = (
#             "title",
#             "description",
#         )

#     def get_description(self, obj):
#         return mark_safe(obj.description)


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ('number',)
    
