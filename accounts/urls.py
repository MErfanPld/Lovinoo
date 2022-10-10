from django.urls import include, path

from accounts.api.urls import urlpatterns

from .views import (AddNewAdminView, AdminListView, AdminLoginView, LogoutView,
                    UserDeleteView, UserDetailView, UserListView)

app_name = "accounts"

urlpatterns = [
    path("login/", AdminLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("admin_list/", AdminListView.as_view(), name="admin_list"),
    path("user_list/", UserListView.as_view(), name="user_list"),
    path("admin_create/", AddNewAdminView.as_view(), name="admin_create"),
    path("delete/<int:pk>/", UserDeleteView.as_view(), name="delete"),
    path("user_detail/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("api/", include(urlpatterns)),
]
