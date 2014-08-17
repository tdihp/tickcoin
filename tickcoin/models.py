from django.db import models


# Create your models here.
class Slot(models.Model):
    user = models.ForeignKey('auth.User', null=False)
    name = models.CharField(max_length=32, null=False)

    class Meta:
        unique_together = [['user', 'name']]


class Tick(models.Model):
    slot = models.ForeignKey(Slot, null=False)
    tick_time = models.DateTimeField(auto_now=True)
