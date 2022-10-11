from django.contrib import admin

from .models import Favorite, Block, ReportedUser, Seen

# Register your models here.
admin.site.register(Favorite)
admin.site.register(Block)
admin.site.register(ReportedUser)
admin.site.register(Seen)
