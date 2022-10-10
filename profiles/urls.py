from django.urls import include, path

from profiles.api.urls import urlpatterns

app_name = "profiles"

urlpatterns = [
    path("api/", include(urlpatterns)),
]
