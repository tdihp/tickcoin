from django.contrib import admin

# Register your models here.
from tickcoin import models

admin.site.register(models.Slot)
admin.site.register(models.Tick)
