from django.db import models


# Create your models here.
class Slot(models.Model):
    user = models.ForeignKey('auth.User')
    name = models.CharField(max_length=64)


class Tick(models.Model):
    slot_id = models.ForeignKey(Slot)
    tick_time = models.DateTimeField(auto_now=True)
