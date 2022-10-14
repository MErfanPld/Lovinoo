from django.urls import include, path

from config.api.urls import urlpatterns

from .views import (ContactDetailView,
                    ContactListView, PanelView, LandingView)

from .views import (AboutUsCreateView, AboutUsView, ContactDetailView,
                PanelView, RuleCreateView, RuleView, LandingView)


app_name = "config"

urlpatterns = [
    path("about_us/", AboutUsView.as_view(), name="about_us"),
    path("about_create/", AboutUsCreateView.as_view(), name="about_create"),
    path("rule_create/", RuleCreateView.as_view(), name="rule_create"),
    path("rule/", RuleView.as_view(), name="rule"),
    path("contact_list/", ContactListView.as_view(), name="contact_list"),
    path(
        "contact_detail/<int:pk>/", ContactDetailView.as_view(), name="contact_detail"
    ),
    path("api/", include(urlpatterns)),
    path("panel/", PanelView.as_view(), name="panel"),
    path("", LandingView.as_view(), name="landing"),
]
