from django.urls import path

from .views import (CityListApiView, ContactUsCreateAPiView,
                    RateApiView)

# from .views import (CityListApiView, ContactUsCreateAPiView,
#                     RuleApiView, PrivacyApiView, AboutUsApiView,RateApiView)

app_name = "config"
urlpatterns = [
    # path("rule/", RuleApiView.as_view()),
    path("city_list/", CityListApiView.as_view()),
    path("contact_us/", ContactUsCreateAPiView.as_view()),
    # path("privacy/", PrivacyApiView.as_view()),
    # path("aboutus/", AboutUsApiView.as_view()),
      path("rate/", RateApiView.as_view()),

]
