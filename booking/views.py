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
    first_week = []
    for i in range(0, 7):
        date = first_date + datetime.timedelta(days=i - weekday)
        title = f'{weekdays.get(i)} {date.strftime("%d.%m.%Y")}'
        book_object, status = Booking.objects.get_or_create(day=date, defaults={'title': title})
        first_week.append(book_object)
    week_list = [first_week]

    # цикл сколько недель нужно после основной
    for count in range(0, 3):
        book_list = []
        for key in weekdays:
            date += datetime.timedelta(days=1)
            title = f'{weekdays.get(key)} {date.strftime("%d.%m.%Y")}'
            book_object, status = Booking.objects.get_or_create(day=date, defaults={'title': title})
            book_list.append(book_object)

        week_list.append(book_list)
    # конец цикла

    context = {'booking_main': first_week, 'booking_second': book_list, 'weeks': week_list}
    return HttpResponse(template.render(context, request))


