from django.urls import path

from .views import (ImageDeleteApiView, ProfileApiView, ProfileFilterApiView,
                    ProfileListApiView, ProfileSearchApiView,
                    UserImageUploadApiView,UserStatusApiView,ProfileDetailApiView, ImageOrdering)

urlpatterns = [
    path("", ProfileApiView.as_view()),
    path("list/", ProfileListApiView.as_view()),
    path("upload_image/", UserImageUploadApiView.as_view()),
    path(
        "delete_image/<int:pk>/",
        ImageDeleteApiView.as_view(),
    ),
    path("filter/", ProfileFilterApiView.as_view()),
    path("image_filter/", ImageOrdering.as_view()),
    path("search/", ProfileSearchApiView.as_view()),
    path('status/',UserStatusApiView.as_view()),
    path("detail/<int:id>/",ProfileDetailApiView.as_view())
]
