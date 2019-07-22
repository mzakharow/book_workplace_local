import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse

from booking.forms import LoginForm
from booking.models import Booking, RoleList, DutyAdmin


@login_required
def index(request):
    template = loader.get_template('booking/index.html')
    first_date = datetime.date.today()
    weekday = datetime.datetime.now().weekday()
    weekdays = {0: 'ПН', 1: 'ВТ', 2: 'СР', 3: 'ЧТ', 4: 'ПТ', 5: 'СБ', 6: 'ВС'}
    first_week = []
    for i in range(0, 7):
        date = first_date + datetime.timedelta(days=i - weekday)
        title = f'{weekdays.get(i)} {date.strftime("%d.%m.%Y")}'
        book_object, status = Booking.objects.get_or_create(day=date, defaults={'title': title})
        if status and book_object.day.weekday() < 5:
            users = list(User.objects.all())
            book_object.user.add(*users)
            book_object.free_places -= len(users)
            book_object.save()
        first_week.append(book_object)
    week_list = [first_week]

    for count in range(0, 2):
        book_list = []
        for key in weekdays:
            date += datetime.timedelta(days=1)
            title = f'{weekdays.get(key)} {date.strftime("%d.%m.%Y")}'
            book_object, status = Booking.objects.get_or_create(day=date, defaults={'title': title})
            if status and book_object.day.weekday() < 5:
                users = list(User.objects.all())
                book_object.user.add(*users)
                book_object.free_places -= len(users)
                book_object.save()
            book_list.append(book_object)

        week_list.append(book_list)

    today = datetime.date.today()

    role_list = list(RoleList.objects.all())
    duty_admin = list(DutyAdmin.objects.all())
    duty_list = list()
    for admin in duty_admin:
        duty_list.insert(admin.day, admin.administrator)
    context = {'weeks': week_list, 'today': today, 'role_list': role_list, 'duty_admin': duty_admin}

    return HttpResponse(template.render(context, request))


def login_view(request):
    form = LoginForm(request.POST or None)

    if form.is_valid():
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        # user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        login(request, user=user)
        return HttpResponseRedirect(reverse('index'))
    context = {
        'form': form,
    }
    return render(request, 'booking/login.html', context)


def reserve_view(request, str_date):
    date = datetime.datetime.strptime(str_date, "%Y-%m-%d")
    book_object = Booking.objects.get(day=date)
    if request.user not in book_object.user.all() and book_object.free_places > 0:
        book_object.user.add(request.user)
        book_object.free_places -= 1
        book_object.save()
    return HttpResponseRedirect(reverse('index'))


def unreserve_view(request, str_date):
    date = datetime.datetime.strptime(str_date, "%Y-%m-%d")
    book_object = Booking.objects.get(day=date)
    book_object.user.remove(request.user)
    book_object.free_places += 1
    book_object.save()
    return HttpResponseRedirect(reverse('index'))

