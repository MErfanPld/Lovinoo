from django.conf import settings
from django.db import models
from django_extensions.db.models import TimeStampedModel

user = settings.AUTH_USER_MODEL


# Create your models here.
class Tariff(models.Model):
    title = models.CharField(max_length=255)
    price = models.IntegerField()
    time = models.IntegerField()

    def __str__(self):
        return f"{self.title}-{self.price}"


class OriginCart(models.Model):
    number = models.CharField(max_length=16)


class CartPay(TimeStampedModel):
    class STATUS(models.TextChoices):
        waiting = "waiting", " در انتظار تایید"
        accepted = "accepted", "تایید شده"
        rejected = "rejected", " تایید نشد"

    user = models.ForeignKey(
        user, on_delete=models.CASCADE, related_name="cart_pays", null=True, blank=True
    )
    name = models.CharField(max_length=255)
    time = models.DateTimeField()
    tracing_number = models.CharField(max_length=20)
    image = models.ImageField(upload_to="cart_pay/")
    description = models.TextField(blank=True)
    cart_number = models.CharField(max_length=16)
    origin_cart = models.ForeignKey(OriginCart, on_delete=models.PROTECT)
    tariff = models.ForeignKey(Tariff, on_delete=models.PROTECT)
    status = models.CharField(max_length=15, choices=STATUS.choices, default="waiting")


class PayHistory(models.Model):
    user = models.ForeignKey(
        user,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="pays",
    )
    price = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    tariff = models.CharField(max_length=125)
    authority = models.CharField(null=True, blank=True, max_length=100)
