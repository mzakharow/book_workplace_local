from django.conf import settings
from django.db import models


class Booking(models.Model):
    title = models.CharField(max_length=64)
    day = models.DateField()
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    class Meta:
        ordering = ['-day']

