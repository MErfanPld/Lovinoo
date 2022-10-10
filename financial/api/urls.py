from django.urls import path

from .views import (CartPayCreateApiView, TariffListApiView,
                    UserCartPayApiView, UserHistoryPay, CartPayView, VerifyPayView)

urlpatterns = [
    path("", TariffListApiView.as_view()),
    path("cart_pay/", CartPayCreateApiView.as_view()),
    path("user_cart_pay/", UserCartPayApiView.as_view()),
    path("user_pay/", UserHistoryPay.as_view()),
    path("user_pay/", UserHistoryPay.as_view()),
    path('pay/<int:pk>/', CartPayView.as_view()),
    path('verify/', VerifyPayView.as_view()),
]
