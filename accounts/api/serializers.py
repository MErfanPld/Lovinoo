from rest_framework import serializers


class AuthSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)


class VerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)
    code = serializers.CharField(max_length=6)
    fcm_token = serializers.CharField()
