from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save

from profiles.models import Profile

user = get_user_model()


def create_profile(sender, **kwargs):
    if kwargs["created"] and not kwargs["instance"].is_admin:
        p1 = Profile(user=kwargs["instance"])
        p1.save()


def got_online(sender, user, request, **kwargs):
    user.profile.is_online = True
    user.profile.save()


def got_offline(sender, user, request, **kwargs):
    user.profile.is_online = False
    user.profile.save()


post_save.connect(receiver=create_profile, sender=user)
user_logged_in.connect(receiver=got_online, sender=user_logged_in)
user_logged_out.connect(receiver=got_offline, sender=user_logged_out)
