import calendar
import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from booking.models import Booking


def index(request):
    template = loader.get_template('booking/index.html')
    first_date = datetime.datetime.now()
    weekday = datetime.datetime.now().weekday()
    weekdays = {0: 'ПН', 1: 'ВТ', 2: 'СР', 3: 'ЧТ', 4: 'ПТ', 5: 'СБ', 6: 'ВС'}
    book_list = []
    for i in range(0, 7):
        date = first_date + datetime.timedelta(days=i - weekday)
        title = f'{weekdays.get(i)} {date.strftime("%d.%m.%Y")}'
        book_object, status = Booking.objects.get_or_create(day=date, defaults={'title': title})
        book_list.append(book_object)

    context = {'booking': book_list}
    return HttpResponse(template.render(context, request))


