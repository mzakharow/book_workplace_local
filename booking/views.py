import calendar
import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from booking.models import Booking


def index(request):
    template = loader.get_template('booking/index.html')
    # booking = Booking.objects.order_by('day')
    first_date = datetime.datetime.now()
    weekday = datetime.datetime.now().weekday()
    days = 20 - weekday  # 3 weeks, exclude previous days
    last_date = datetime.datetime.now() + datetime.timedelta(days=days)
    booking = Booking.objects.filter(day__range=(first_date, last_date))
    weekdays = {0: 'ПН', 1: 'ВТ', 2: 'СР', 3: 'ЧТ', 4: 'ПТ', 5: 'СБ', 6: 'ВС'}
    book_dict = {}
    book_list = []
    for i in range(0, 7):
        if weekday > i:
            # book_dict[i] = {weekdays.get(i)}
            book_list.append({'title': weekdays.get(i)})
        # elif weekday == i:
        #     book_object = Booking.objects.filter(day=first_date)
        #     if book_object.exists():
        #         book_dict[i] = book_object
        #     else:
        #         book_dict[i] = empty_day(first_date + datetime.timedelta(days=i-weekday))
        else:
            book_object = Booking.objects.filter(day=first_date + datetime.timedelta(days=i-weekday))
            if book_object.exists():
                book_list.append({'title': weekdays.get(i), 'object': book_object})
            else:
                book_list.append({'title': weekdays.get(i),
                                  'object': empty_day(first_date + datetime.timedelta(days=i-weekday))})

    # for i in range(0, 14):
    #     if weekday > i:
    #         book_list = {i:}
    #     pass
    context = {'booking': book_list, 'weekday': weekday}
    return HttpResponse(template.render(context, request))
    # return HttpResponse(calendar.LocaleHTMLCalendar().formatmonth(2019, 4))


def empty_day(date):

    if date.day < 10:
        day = f'0{str(date.day)}'
    else:
        day = str(date.day)
    if date.month < 10:
        month = f'0{str(date.month)}'
    else:
        month = str(date.month)

    return Booking.objects.create(title=f'{day}.{month}.{str(date.year)}', day=date)
