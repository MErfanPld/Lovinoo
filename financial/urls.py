from django.urls import include, path

from financial.api.urls import urlpatterns

from .views import (CartPayAcceptedListView, CartPayNotConfirmedListView,
                    OriginCartCreateView, OriginCartListView, OriginDeleteView,
                    OriginUpdateView, PayHistoryListView, TariffCreateView,
                    TariffDeleteView, TariffListView, TariffUpdateView)

app_name = "financial"
urlpatterns = [
    path("tarrif_list/", TariffListView.as_view(), name="tariff_list"),
    path("tarrif_create/", TariffCreateView.as_view(), name="tariff_create"),
    path("tarrif_update/<int:pk>/", TariffUpdateView.as_view(), name="tariff_update"),
    path("tarrif_delete/<int:pk>/", TariffDeleteView.as_view(), name="tariff_delete"),
    path("origin_list/", OriginCartListView.as_view(), name="origin_list"),
    path("origin_create/", OriginCartCreateView.as_view(), name="origin_create"),
    path("origin_update/<int:pk>/", OriginUpdateView.as_view(), name="origin_update"),
    path("origin_delete/<int:pk>/", OriginDeleteView.as_view(), name="origin_delete"),
    path("pay_list/", PayHistoryListView.as_view(), name="pay_history"),
    path("cart_pay/", CartPayAcceptedListView.as_view(), name="cart_pay"),
    path("cart_pay_wait/", CartPayNotConfirmedListView.as_view(), name="cart_pay_wait"),
    path("api/", include(urlpatterns)),
]
