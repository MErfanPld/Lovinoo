from django.urls import include, path

from chat.api.urls import urlpatterns

app_name = "chat"
urlpatterns = [
    path("api/", include(urlpatterns)),
]
