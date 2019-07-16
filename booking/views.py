import calendar

from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from booking.models import Booking


def index(request):
    template = loader.get_template('booking/index.html')
    booking = Booking.objects.order_by('day')
    context = {'booking': booking}
    return HttpResponse(template.render(context, request))
    # return HttpResponse(calendar.LocaleHTMLCalendar().formatmonth(2019, 4))
