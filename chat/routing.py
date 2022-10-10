from django.urls import re_path

from .consumers import EchoConsumer

websocket_urlpatterns = [re_path("ws/", EchoConsumer.as_asgi())]
