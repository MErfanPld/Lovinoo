from django.urls import path

from .views import (
    DeleteRoomApiView,
    MessageDeleteView,
    MessageUpdateApiView,
    RoomApiView,
    RoomCreateApiView,
    UserRoomApiView,
)

urlpatterns = [
    path("room/<int:pk>/", RoomApiView.as_view()),
    path("create/", RoomCreateApiView.as_view()),
    path("message_delete/", MessageDeleteView.as_view()),
    path("message_update/<int:pk>/", MessageUpdateApiView.as_view()),
    path("user_room/", UserRoomApiView.as_view()),
    path("room_delete/", DeleteRoomApiView.as_view()),
]
