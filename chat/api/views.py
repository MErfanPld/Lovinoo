from django.contrib.auth import get_user_model
from django.db.models import Subquery

from rest_framework import status
from rest_framework.generics import (
    DestroyAPIView,
    GenericAPIView,
    ListAPIView,
    UpdateAPIView,
)
from rest_framework.response import Response
from ordered_set import OrderedSet

from ..models import Message, Room
from .serializerrs import MessageSerializer, RoomCreateSerializer, UserRoomSerializer
from ..utils import send_notification

user = get_user_model()


class RoomCreateApiView(GenericAPIView):
    serializer_class = RoomCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            context = {
                "is_done": True,
                "message": "چت ساخته شد و پیام ارسال شد",
                "data": serializer.data,
            }
            # user_obj = serializer.validated_data["participate"]
            # user_fcm = user.objects.exclude(id=user_obj).first().fcm_token
            # shown_message = serializer.validated_data['body'] if serializer.validated_data["body"] else "پیام جدید"
            # send_notification([user_fcm, ], 'پیام جدید')
            return Response(data=context, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomApiView(GenericAPIView):
    serializer_class = MessageSerializer

    def get(self, request, *args, **kwargs):
        room_id = kwargs.get("pk")
        chat_list = Message.objects.filter(
            room_id=room_id).order_by("-timestamp")
        date_list = {}
        for item in chat_list:
            date_list[item.timestamp.strftime("%d-%b-%Y")] = []
            for message in chat_list:
                if message.timestamp.strftime('%d-%b-%Y') == item.timestamp.strftime('%d-%b-%Y'):
                    date_list[item.timestamp.strftime("%d-%b-%Y")].append(MessageSerializer(
                        instance=Message.objects.get(id=message.id), context={"request": request}).data)
        chat_list.exclude(author=request.user, read=False).update(read=True)
        context = {
            "is_done": True,
            "message": "لیست  های چت",
            "data": date_list
        }
        return Response(data=context, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            obj = serializer.save(
                room_id=kwargs.get("pk"), author=request.user)
            context = {
                "is_done": True,
                "message": "پبام با موفقیت ارسال شد",
                "data": serializer.data,
            }
            data = ""
            if obj.body:
                data = obj.body
            elif obj.voice:
                data = obj.voice.url
            else:
                data = obj.image.url
            room_participation = Room.objects.get(id=kwargs.get("pk"))
            for receiver in room_participation.participants.all():
                if receiver.id != request.user.id:
                    send_notification([receiver.fcm_token, ], data)

            # user_obj = room_participation.participants.all().exclude(id=self.response.user.id)
            # print(user_obj.exclude(user_id=self.response.user.id))
            # except:
            #     user_obj = room_participation.participants.all()
            #     print(user_obj)
            # # user_obj = room_participation.participants.all().exclude(id=self.response.user.id)
            # print(user_obj.exclude(user_id=self.response.user.id))
            # user_fcm = user.objects.get(id=user_obj).fcm_token
            # send_notification([user_obj, ], "پیام جدید")

            return Response(data=context, status=status.HTTP_201_CREATED)
        context = {
            "is_done": False,
            "message": "خطا در ارسال پیام",
            "data": serializer.data,
        }
        return Response(data=context, status=status.HTTP_400_BAD_REQUEST)


class DeleteRoomApiView(GenericAPIView):
    def get_queryset(self):
        return self.request.user.rooms.all()

    def delete(self, request, *args, **kwargs):
        try:
            chat_list = (request.GET.getlist('chat_id'))
            self.get_queryset().filter(id__in=chat_list).delete()
            return Response(data={"is_done": True, "message": "چت حذف شد"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"is_done": False, "message": e}, status=status.HTTP_400_BAD_REQUEST)


class UserRoomApiView(ListAPIView):
    serializer_class = UserRoomSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        user_chat_list = Room.objects.filter(
            participants__in=[self.request.user])
        chat_list_id = list(OrderedSet(
            Message.objects.filter(room_id__in=user_chat_list).order_by('timestamp').values_list('room_id', flat=True)))
        qs_sorted = list()
        for id in chat_list_id:
            qs_sorted.append(Room.objects.get(id=id))
        return qs_sorted

    def list(self, request, *args, **kwargs):
        response = super(UserRoomApiView, self).list(request, *args, **kwargs)
        context = {"data": response.data, "message": "لیست چت های کاربر"}
        return Response(data=context, status=status.HTTP_200_OK)


class MessageDeleteView(GenericAPIView):
    serializer_class = MessageSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        return Message.objects.filter(author=self.request.user)

    def delete(self, request, *args, **kwargs):
        try:
            message_list = (request.GET.getlist('message_id'))
            self.get_queryset().filter(id__in=message_list).delete()
            return Response(data={"is_done": True, "message": "پیام حذف شد"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"is_done": False, "message": e}, status=status.HTTP_400_BAD_REQUEST)


class MessageUpdateApiView(UpdateAPIView):
    serializer_class = MessageSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        return Message.objects.filter(author=self.request.user)

    def update(self, request, *args, **kwargs):
        super(MessageUpdateApiView, self).update(request, *args, **kwargs)
        return Response(
            data={"message": "پیام با موفقیت به روزرسانی شد"}, status=status.HTTP_200_OK
        )
