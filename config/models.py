from ckeditor.fields import RichTextField
from django.db import models
from django.core.validators import MaxValueValidator
from django.conf import settings

user = settings.AUTH_USER_MODEL
# Create your models here.


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(SingletonModel, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()


# class ConfigBase(SingletonModel):
#     title = models.CharField(max_length=125)
#     description = RichTextField()

#     def __str__(self):
#         return self.title


# class Rules(ConfigBase):
#     pass


# class AboutUs(ConfigBase):
#     pass


# class Privacy(ConfigBase):
#     pass


class Contact(models.Model):
    title = models.CharField(max_length=255)
    email = models.EmailField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    

class Rate(models.Model):
    number = models.PositiveIntegerField(validators=[MaxValueValidator(5)])
    user = models.OneToOneField(user, on_delete=models.CASCADE, related_name='rate')
    
