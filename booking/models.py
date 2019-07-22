from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
# from .managers import PersonManager


class Booking(models.Model):
    title = models.CharField(max_length=64)
    day = models.DateField()
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='user_list')
    home = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='home_list')
    vacant = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='vacant_list')
    free_places = models.IntegerField(blank=True, validators=[MaxValueValidator(14)], default=14)

    class Meta:
        ordering = ['-day']


class RoleList(models.Model):
    title = models.CharField(max_length=24, unique=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)


# class Person(User):
#     objects = models.CharField
#
#     class Meta:
#         proxy = True
#         ordering = ('first_name', )
#
#     def do_something(self):
#         ...