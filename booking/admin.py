from django.contrib import admin
from booking.models import Booking, RoleList, DutyAdmin


class BookingAdmin(admin.ModelAdmin):
    list_display = ['title', 'day']


class RoleListAdmin(admin.ModelAdmin):
    list_display = ['title']


class DutyAdministrator(admin.ModelAdmin):
    list_display = ['title', 'administrator']


admin.site.register(Booking, BookingAdmin)
admin.site.register(RoleList, RoleListAdmin)
admin.site.register(DutyAdmin, DutyAdministrator)
