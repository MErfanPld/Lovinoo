from rest_framework import serializers

from ..models import CartPay, PayHistory, Tariff


class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = ("id","title", "price", "time")


class CartPaySerializer(serializers.ModelSerializer):
    class Meta:
        model = CartPay
        fields = (
            "user",
            "name",
            "time",
            "tracing_number",
            "image",
            "description",
            "cart_number",
            "origin_cart",
            "tariff",
            "status",
        )
        read_only_fields = (
            "user",
            "status",
        )


class PayHistorySerializers(serializers.ModelSerializer):
    class Meta:
        model = PayHistory
        fields = (
            "user",
            "price",
            "date",
            "tariff",
        )
