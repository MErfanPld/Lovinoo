from django.conf import settings
from django.db import models
from django_jalali.db import models as jmodels

user = settings.AUTH_USER_MODEL


class Message(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey("Room", related_name="messages", on_delete=models.CASCADE)
    body = models.TextField(max_length=500, default="", null=True, blank=True)
    image = models.ImageField(upload_to="chat_image/", null=True, blank=True)
    voice = models.FileField(upload_to="chat_voice/", null=True, blank=True)
    timestamp = jmodels.jDateTimeField()
    read = models.BooleanField(default=False)
    
    
    class Meta:
        ordering = ('-timestamp',)


class Room(models.Model):
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="rooms"
    )

    created_at = models.DateTimeField(verbose_name="Creation Date", auto_now_add=True)
    last_activity = models.DateTimeField(
        verbose_name="Last activity date", auto_now=True
    )
    
    
