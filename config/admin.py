from django.contrib import admin

from .models import AboutUs, Rules, Rate

# Register your models here.

admin.site.register(Rules)
admin.site.register(AboutUs)
admin.site.register(Rate)
