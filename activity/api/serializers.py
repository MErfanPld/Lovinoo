from rest_framework import serializers

from ..models import Block, Favorite, ReportedUser


class ReportedUserSerializers(serializers.ModelSerializer):
    # reported_user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ReportedUser
        fields = (
            "to_user",
            "text",
        )

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


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ("to_user",)
