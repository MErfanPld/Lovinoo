from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.conf import settings

from ..models import Block, Favorite, ReportedUser, Activity
from django.contrib.auth import get_user_model

User = get_user_model()


class ReportedUserSerializers(serializers.ModelSerializer):
    # reported_user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ReportedUser
        fields = (
            "to_user",
            "text",
        )

    def validate(self, attrs):
        if self.context['request'].user == attrs.get('to_user'):
            raise serializers.ValidationError(
                f"Users cannot Report themselves.")

        if ReportedUser.objects.filter(to_user=attrs.get('to_user'), from_user=self.context['request'].user).exists():
            raise serializers.ValidationError(
                f"You have already reported this user")

        return super().validate(attrs)

    # def get_reported_user(self,obj):
    #     if not  hasattr(obj,'id'):
    #         return None
    #     if not isinstance(obj,ReportedUser):
    #         return None
    #     return obj.reporteds_usere


class BlockCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ("to_user",)

    def validate(self, attrs):
        if self.context['request'].user == attrs.get('to_user'):
            raise serializers.ValidationError(
                f"Users cannot Block themselves.")

        if Block.objects.filter(to_user=attrs.get('to_user'), from_user=self.context['request'].user).exists():
            raise serializers.ValidationError(
                f"You have already blocked this user")

        return super().validate(attrs)


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ("to_user",)
