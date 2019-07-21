from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models


class Booking(models.Model):
    title = models.CharField(max_length=64)
    day = models.DateField()
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    free_places = models.PositiveIntegerField(blank=True, validators=[MaxValueValidator(14)], default=14)

    class Meta:
        ordering = ['-day']

