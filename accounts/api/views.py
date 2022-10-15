import random

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import authentication, generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..models import OtpCode
from ..utils import send_otp
from .serializers import AuthSerializer, VerifySerializer

user = get_user_model()


# class UserApiView(
#     mixins.CreateModelMixin,
#     mixins.ListModelMixin,
#     mixins.RetrieveModelMixin,
#     generics.GenericAPIView):
#     serializer_class =
#     queryset =
#     lookup_field =
#     permission_classes = [permissions.IsAuthenticated]
#     authentication_classes = [authentication.SessionAuthentication]
#
#     def get(self, request, *args, **kwargs):
#         pk = kwargs.get('pk')
#         if pk:
#             return self.retrieve(request, *args, **kwargs)
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#     def perform_create(self, serializer):
#         serializer.save()


class AuthApiView(generics.GenericAPIView):
    serializer_class = AuthSerializer
    permission_classes = [
        AllowAny,
    ]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            random_code = random.randint(000000, 999999)
            phone_number = serializer.validated_data["phone_number"]
            OtpCode.objects.create(phone_number=phone_number, code=random_code)
            send_otp(phone_number=phone_number, code=random_code)
            context = {
                "is_done": True,
                "message": "پیام ارسال شد",
                "data": serializer.data,
            }
            return Response(data=context, status=status.HTTP_200_OK)
        context = {
            "is_done": False,
            "message": "خطا در پارامتر ارسالی",
            "data": serializer.errors,
        }
        return Response(data=context, status=status.HTTP_400_BAD_REQUEST)


class VerifyApiView(generics.GenericAPIView):
    serializer_class = VerifySerializer
    permission_classes = [
        AllowAny,
    ]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone_number = serializer.validated_data["phone_number"]
            code = serializer.validated_data["code"]
            otp_obj = OtpCode.objects.filter(phone_number=phone_number).last()
            if otp_obj and otp_obj.code == code:
                try:
                    user_obj = user.objects.get(phone_number=phone_number)
                    user_obj.fcm_token = serializer.validated_data["fcm_token"]
                    user_obj.save()
                    token, created = Token.objects.get_or_create(user=user_obj)
                    context = {
                        "is_done": True,
                        "message": "کاربر با موفقیت وارد شد",
                        "token": token.key,
                    }
                    return Response(data=context, status=status.HTTP_200_OK)
                except user.DoesNotExist:
                    fcm_token = serializer.validated_data["fcm_token"]
                    user_obj = user.objects.create_user(phone_number=phone_number,fcm_token=fcm_token)
                    token_obj = Token.objects.create(user=user_obj)
                    context = {
                        "is_done": True,
                        "message": "کاربر با موفیت ساخته شد",
                        "token": token_obj.key,
                    }
                    return Response(data=context, status=status.HTTP_200_OK)
            else:
                context = {
                    "is_done": False,
                    "message": "کد ارسال برای کاربر با کد ذزیافتی همخوانی ندارد",
                }
                return Response(data=context, status=status.HTTP_400_BAD_REQUEST)
        context = {
            "is_done": False,
            "message": "خطا در پارامتر ارسالی",
        }
        return Response(data=context, status=status.HTTP_400_BAD_REQUEST)


class LogoutApiView(generics.GenericAPIView):
    @staticmethod
    def delete(request, *args, **kwargs):
        request.user.auth_token.delete()
        context = {
            "is_done": True,
            "message": "token کاربر با موفقیت حذف شد",
        }
        return Response(data=context, status=status.HTTP_200_OK)


class DeleteAccountApiView(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        user_obj = get_object_or_404(user, id=request.user.id)
        user_obj.delete()
        return Response(data={
            "is_done": True,
            "message": "کاربر با موفقیت حذف شد",
        })
