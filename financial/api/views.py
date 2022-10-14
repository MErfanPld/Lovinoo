import json
import requests
from lovinoo.celery import app
from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.views.generic import View
from ..models import CartPay, Tariff, PayHistory
from .serializers import (CartPaySerializer, PayHistorySerializers,
                          TariffSerializer)
from celery import shared_task


@shared_task
def connect_gateway(price, phone):
    req_data = {
        "merchant_id": MERCHANT,
        "amount": price,
        "callback_url": CallbackURL,
        "description": description,
        "metadata": {"mobile": phone}
    }
    req_header = {"accept": "application/json",
                  "content-type": "application/json'"}
    req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
        req_data), headers=req_header)
    return req


class TariffListApiView(ListAPIView):
    serializer_class = TariffSerializer
    queryset = Tariff.objects.all()

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response(
            {"is_done": True, "message": "لیست تغرفه ها", "data": response.data}
        )


class CartPayCreateApiView(CreateAPIView):
    serializer_class = CartPaySerializer
    queryset = CartPay.objects.all()

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"is_done": True, "data": response.data})


class UserCartPayApiView(ListAPIView):
    serializer_class = CartPaySerializer

    def get_queryset(self):
        cart_pays = self.request.user.cart_pays.all()
        return cart_pays

    def list(self, request, *args, **kwargs):
        response = super(UserCartPayApiView, self).list(
            request, *args, **kwargs)
        return Response({"is_done": True, "data": response.data})


class UserHistoryPay(ListAPIView):
    serializer_class = PayHistorySerializers

    def get_queryset(self):
        cart_pays = self.request.user.pays.all()
        return cart_pays

    def list(self, request, *args, **kwargs):
        response = super(UserHistoryPay, self).list(request, *args, **kwargs)
        return Response({"is_done": True, "data": response.data})


MERCHANT = '0af09ec7-5cfe-4d7c-9356-f23447eb680b'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"
CallbackURL = 'https://lovino.darkube.app/financial/api/verify/'


class CartPayView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        tariff_obj = Tariff.objects.get(id=kwargs.get('pk'))
        # req = connect_gateway.delay(tariff_obj.price, request.user.phone_number)
        req = connect_gateway(tariff_obj.price, request.user.phone_number)
        authority = req.json()['data']['authority']
        PayHistory.objects.create(user=self.request.user, price=tariff_obj.price, tariff=tariff_obj.title,
                                  authority=authority)
        context = {
            'is_done': True,
            'message': "در حال انتقال به درگاه پرداخت",
            'data': ZP_API_STARTPAY.format(authority=authority)
        }
        return Response(data=context, status=status.HTTP_200_OK)


class VerifyPayView(GenericAPIView):
    permission_classes = [AllowAny, ]
    def get(self, request):
        t_status = request.GET.get('Status')
        t_authority = request.GET['Authority']
        pay_history_obj = PayHistory.objects.get(authority=t_authority)
        if request.GET.get('Status') == 'OK':
            req_header = {"accept": "application/json",
                          "content-type": "application/json'"}
            req_data = {
                "merchant_id": MERCHANT,
                "amount": pay_history_obj.price,
                "authority": t_authority
            }
            req = requests.post(url=ZP_API_VERIFY, data=json.dumps(
                req_data), headers=req_header)
            if len(req.json()['errors']) == 0:
                t_status = req.json()['data']['code']
                if t_status == 100:
                    return redirect('/financial/api/paymentok/')
                elif t_status == 101:
                    return redirect('/financial/api/paymentno/')
                else:
                    PayHistory.objects.get(authority=t_authority).delete()
                    return redirect('/financial/api/paymentok/')
            else:
                PayHistory.objects.get(authority=t_authority).delete()
                return redirect('/financial/api/paymentok/')
        else:
            PayHistory.objects.get(authority=t_authority).delete()
            return redirect('/financial/api/paymentok/')


class Paymentok(View):
    def get(self, request, *args, **kwargs):
        return render(request,'../templates/financial/paymentok.html')

class Paymentno(View):
    def get(self, request, *args, **kwargs):
        return render(request,'../templates/financial/paymentno.html')

