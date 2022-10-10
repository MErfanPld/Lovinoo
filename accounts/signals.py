from django.contrib.auth.signals import user_logged_in, user_logged_out


def got_online(sender, user, request, **kwargs):
    user.is_online = True
    user.save()


def got_offline(sender, user, request, **kwargs):
    user.is_online = False
    user.save()


user_logged_in.connect(receiver=got_online, sender=user_logged_in)
user_logged_out.connect(receiver=got_offline, sender=user_logged_out)
