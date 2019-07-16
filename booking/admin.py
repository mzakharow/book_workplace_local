from django.contrib import admin
from booking.models import Booking


class BookingAdmin(admin.ModelAdmin):
    list_display = ['title', 'day']


admin.site.register(Booking, BookingAdmin)
