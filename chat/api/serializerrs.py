from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from activity.models import Block
from profiles.api.serializers import ProfileMainSerializer
from ..models import Message, Room
from ..utils import send_notification

user = get_user_model()


# class RoomSerializer(serializers.ModelSerializer):
#     last_message = serializers.SerializerMethodField()
#     fcm_token = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Room
#         fields = (
#             "participants",
#             "created_at",
#             "id",
#             "last_message",
#             "fcm_token",
#         )
#         read_only_fields = (
#             "id",
#             "want_data",
#             "fcm_token",
#             "created_at",
#             "last_message",
#         )
#
#     def get_fcm_token(self, obj):
#         for user in obj.participants.all():
#             if User.objects.get(id=user.id).fcm_token != obj.want.user.fcm_token:
#                 return {
#                     "owner": User.objects.get(id=user.id).fcm_token,
#                     "customer": obj.want.user.fcm_token,
#                 }
#
#     def get_last_message(self, obj):
#         return UserMessageSerializer(obj.messages.last()).data


class RoomCreateSerializer(serializers.ModelSerializer):
    participate = serializers.IntegerField(write_only=True)

    class Meta:
        model = Message
        fields = (
            "id",
            "author",
            "room",
            "body",
            "image",
            "voice",
            "timestamp",
            "participate",
        )
        read_only_fields = ("id", "author", "room", "participate", "read")

    def create(self, validated_data):
        participate = validated_data.pop("participate")
        other_user = get_object_or_404(user, id=participate)
        room_obj = Room()
        room_obj.save()
        room_obj.participants.add(self.context["request"].user, other_user)
        room_obj.save()
        obj = message = Message.objects.create(
            room=room_obj, author=self.context["request"].user, **validated_data
        )
        data = ""
        if obj.body:
            data = obj.body
        elif obj.voice:
            data = obj.voice.url if obj.voice else None
        else:
            data = obj.image.url if obj.image else None
        send_notification([other_user.fcm_token, ], data)
        return message


class MessageSerializer(serializers.ModelSerializer):
    is_me = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = (
            "id",
            "author",
            "room",
            "body",
            "image",
            "voice",
            "timestamp",
            "read",
            "is_me",
        )
        read_only_fields = (
            "id",
            "author",
            "room",
            "is_me",
        )

    def get_is_me(self, obj):
        user = self.context['request'].user
        if obj.author.id == user.id:
            return True
        return False


class MessageMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            "id",
            "author",
            "room",
            "body",
            "image",
            "voice",
            "timestamp",
            "read",
        )
        read_only_fields = (
            "id",
            "author",
            "room",
        )


class UserRoomSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    unread_message = serializers.SerializerMethodField()
    partner_info = serializers.SerializerMethodField()

    # fcm_token=serializers.SerializerMethodField()
    class Meta:
        model = Room
        fields = (
            "id",
            "participants",
            "created_at",
            "last_message",
            'partner_info',
            'unread_message',
            # 'fcm_token',
        )
        read_only_fields = (
            "id",
            # 'fcm_token',
            "created_at",
            'last_message',
            'unread_message',
            'partner_info',
        )
        depth = 2

    #
    # def get_fcm_token(self, obj):
    #     for user in obj.participants.all():
    #         if User.objects.get(id=user.id).fcm_token != obj.want.user.fcm_token:
    #             return {
    #                 'owner': User.objects.get(id=user.id).fcm_token,
    #                 'customer': obj.want.user.fcm_token,
    #             }

    def get_last_message(self, obj):
        last_message = obj.messages.all().last()
        if last_message.image:

            return "عکس"
        elif last_message.voice:

            return "ویس"

        return last_message.body

    def get_partner_info(self, obj):
        blocked_me_users = Block.objects.filter(to_user=self.context['request'].user)\
            .values_list('from_user_id', flat=True)

        for user_obj in obj.participants.all():
            if user_obj.id != self.context['request'].user.id:
                data = ProfileMainSerializer(
                    many=False).to_representation(user_obj.profile)
                if user_obj.id in blocked_me_users:
                    data['is_blocked'] = True
                else:
                    data['is_blocked'] = False
                return data

    def get_unread_message(self, obj):
        user = self.context['request'].user
        Name = ""
        chat_messages = obj.messages.all().exclude(
            author=user).filter(read=False).count()
        return chat_messages

    def check_participants_blocked(self, participants):
        blocked_me_users = Block.objects.filter(to_user=self.context['request'].user)\
            .values_list('from_user_id', flat=True)
        new_participants = []

        for item in participants:
            if item.get('id') in blocked_me_users:
                item['is_blocked'] = True
            else:
                item['is_blocked'] = False

            new_participants.append(item)

        return new_participants

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['messages_count'] = instance.messages.count()
        rep['participants'] = self.check_participants_blocked(
            rep['participants'])
        return
