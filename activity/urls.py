from django.urls import include, path

from activity.api.urls import urlpatterns

from .views import ReportedUserList

app_name = "activity"
urlpatterns = [
    path("reported_user/", ReportedUserList.as_view(), name="reported"),
    path("api/", include(urlpatterns)),
]
