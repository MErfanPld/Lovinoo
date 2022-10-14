import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from activity.models import Favorite
from financial.models import PayHistory, Tariff
from ..models import Image, Profile


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = (
            "id",
            "image",
        )
        read_only_fields = ("id",)


class ProfileMainSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "user_name",
            "province",
            "city",
            "first_name",
            "last_name",
            "bio",
            "gender",
            "birthdate",
            "user_age",
            "profile_image",
            "status",
            "photo",
        )
        read_only_fields = (
            "user",
            "user_age",
            "status",
            "profile_image",
        )

    def get_profile_image(self, obj):
        profile_image = Image.objects.filter(user=obj.user)
        return ProfileImageSerializer(instance=profile_image, many=True).data


class ProfileSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField(read_only=True)
    chat_id = serializers.SerializerMethodField(read_only=True)

    # user=serializers.SerializerMethodField(source='user',read_only=True)
    liked = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "user_name",
            "photo",
            "confirmed_image",
            "province",
            "city",
            "first_name",
            "last_name",
            "bio",
            "gender",
            "birthdate",
            "user_age",
            "profile_image",
            "status",
            "chat_id",
            'liked',
        )
        read_only_fields = (
            "user",
            "user_age",
            "status",
            "chat_id",
            'liked',
        )

    def get_profile_image(self, obj):
        profile_image = Image.objects.filter(user=obj.user)
        return ProfileImageSerializer(instance=profile_image, many=True).data

    def get_chat_id(self, obj):
        user = self.context['request'].user
        requested_user_rooms = user.rooms.all().values_list('id', flat=True)
        obj_rooms = obj.user.rooms.all().values_list('id', flat=True)
        room_id = list(set(requested_user_rooms) & set(obj_rooms))
        if room_id:
            return room_id[0]
        return None

    def get_liked(self, obj):
        user = self.context['request'].user
        favorite_obj = Favorite.objects.filter(
            from_user=user, to_user=obj.user)
        if favorite_obj:
            return True
        return False

    def to_representation(self, instance):
        resp = super().to_representation(instance)
        resp['expire_date'] = instance.user.get_account_expire_days()
        return resp


class ImageSerializer(serializers.Serializer):
    image = Base64ImageField()
