from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CartPay, PayHistory


@receiver(post_save, sender=CartPay)
def create_pay_history(sender, **kwargs):
    if kwargs["instance"].status == "accepted":
        PayHistory.objects.create(
            user=kwargs["instance"].user,
            date=kwargs["instance"].time,
            tariff=kwargs["instance"].tariff.title,
            price=kwargs["instance"].tariff.price,
        )
