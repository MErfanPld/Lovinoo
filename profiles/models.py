import datetime

import jdatetime
from django.conf import settings
from django.core.cache import cache
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    ValidationError)
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django_jalali.db import models as jmodels

user = settings.AUTH_USER_MODEL
from accounts.models import User


# Create your models here.


class ActiveProfileManager(models.Manager):
    def active(self, **kwargs):
        return self.filter(is_activae=True, **kwargs)



class Profile(TimeStampedModel):
    GENDER = (
        ("مرد", "MALE"),
        ("زن", "FEMALE"),
    )
    Status = (
        ("آنلاین", "Online"),
        ("آفلاین", "Offline"),
    )
    user = models.OneToOneField(
        user,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    user_name = models.CharField(blank=True, max_length=125, unique=True, null=True)
    province = models.CharField(
        blank=True,
        max_length=125,
    )
    city = models.CharField(
        blank=True,
        max_length=125,
    )
    first_name = models.CharField(
        blank=True,
        max_length=125,
    )
    last_name = models.CharField(
        blank=True,
        max_length=125,
    )
    bio = models.CharField(
        blank=True,
        max_length=500,
    )
    gender = models.CharField(
        blank=True,
        max_length=10,
        choices=GENDER,
    )
    status = models.CharField(
        default="افلاین",
        max_length=12,
        choices=Status,
    )
    birthdate = models.DateField(
        blank=True,
        null=True,
    )
    age = models.BigIntegerField(
        verbose_name="سن",
        null=True, blank=True
    )
    photo = models.ImageField(upload_to="images/", null=True, blank=True)
    confirmed_image = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = ActiveProfileManager()
    
    
    class Meta:
      ordering=("status",)

    def save(self, *args, **kwargs):
        if not self.user_name:
            self.user_name = None
        if self.birthdate:
            self.age = jdatetime.datetime.today().year - self.birthdate.year
        super().save(*args, **kwargs)

    @property
    def user_age(self):
        if self.birthdate:
            user_age = jdatetime.datetime.today().year - self.birthdate.year
            return user_age

    @property
    def has_image(self):
        if self.images.all().count() > 0:
            return True
        return False


class Image(models.Model):
    image = models.ImageField(upload_to="")
    user = models.ForeignKey(
        user,
        on_delete=models.CASCADE,
        related_name="images",
        blank=True,
        null=True,
    )

    def clean(self):
        user_obj = User.objects.get(id=self.user.id)
        if user_obj.images.count() >= 5:
            raise ValidationError("max image for each user is five")
