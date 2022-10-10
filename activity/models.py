from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django_extensions.db.models import TimeStampedModel

user = settings.AUTH_USER_MODEL


class Activity(TimeStampedModel):
    """BaseModel to represent Activity relationships"""

    from_user = models.ForeignKey(
        user,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_from",
        related_query_name="%(app_label)s_%(class)s_from",
    )
    to_user = models.ForeignKey(
        user,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_to",
        related_query_name="%(app_label)s_%(class)s_to",
    )

    class Meta:
        abstract = True
        unique_together = ("from_user", "to_user")

    def __str__(self):
        return f"{self.from_user}-{self.__class__.__name__}-{self.to_user}"

    def save(self, *args, **kwargs):
        # Ensure users can't block themselves
        if self.from_user == self.to_user:
            raise ValidationError(f"Users cannot {self.__class__.__name__} themselves.")
        super(Activity, self).save(*args, **kwargs)


class Block(Activity):
    pass


class Favorite(Activity):
    pass


class Pined(Activity):
    pass


class ReportedUser(Activity):
    text = models.TextField()

    
    
class Seen(Activity):
    pass    
