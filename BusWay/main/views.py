import calendar
import datetime
import locale
from datetime import datetime
from django.contrib.auth import logout
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import *


def main_page(request):
    routes = []
    title_name = 'Главная страница'
    locale.setlocale(locale.LC_ALL, 'Russian_Russia.utf8')
    today = datetime.today()
    formatted_date = today.strftime('%d %B %Y')

    today = timezone.now()
    upcoming_routes = Route.objects.all()
    for route in upcoming_routes:
        if route.departure_time.date() == today.date():
            schedule = Schedule.objects.get(route=route)
            bus = Bus.objects.get(id=schedule.bus.id)

            routes.append({'schedule': schedule, 'route': route, 'bus': bus})

    context = {
        'routes': routes,
        'today': formatted_date,
        'title': title_name
    }
    return render(request, "main_page/main_page.html", context=context)


def logout_func(request):
    logout(request)
    return redirect('main_page')


def search_routes(request):
    if request.method == 'POST':
        schedule = None
        departure = request.POST.get('departure')
        arrival = request.POST.get('arrival')
        date = request.POST.get('date')

        title = f"Рейсы {departure} - {arrival}"

        if departure:
            departure = departure.strip().capitalize()

        if arrival:
            arrival = arrival.strip().capitalize()
        # Преобразуем дату из строки в объект datetime
        try:
            search_date = datetime.strptime(date, '%Y-%m-%d')
            locale.setlocale(locale.LC_ALL, 'Russian_Russia.utf8')
            formatted_date = search_date.strftime('%d %B')
        except ValueError:
            search_date = None
            formatted_date = None

        # Формируем запрос для фильтрации рейсов
        filtered_routes = Route.objects.all()

        if departure:
            filtered_routes = filtered_routes.filter(origin__icontains=departure)

        if arrival:
            filtered_routes = filtered_routes.filter(destination__icontains=arrival)

        if search_date:
            filtered_routes = filtered_routes.filter(departure_time__date=search_date.date())

        # Получаем список найденных рейсов и связанных данных
        routes = []
        for route in filtered_routes:
            try:
                schedule = Schedule.objects.get(route=route)
                bus = Bus.objects.get(id=schedule.bus.id)
                routes.append({'schedule': schedule, 'route': route, 'bus': bus})
            except (Schedule.DoesNotExist, Bus.DoesNotExist):
                continue

        # Передаем результаты поиска в контекст для отображения
        context = {
            'routes': routes,
            'departure': departure,
            'arrival': arrival,
            'date': date,
            'formatted_date': formatted_date,
            'title': title
        }
        return render(request, 'main_page/bus_routes.html', context=context)

    # В случае GET-запроса (не поступил поиск), просто возвращаем пустую страницу
    return render(request, 'main_page/main_page.html')


def bus_layout(request, schedule_id):
    schedule = Schedule.objects.get(pk=schedule_id)
    bus = get_object_or_404(Bus, pk=schedule.bus.id)
    bus_seats = BusSeat.objects.filter(bus=bus)
    title = 'Выбор места'

    # for i in range(bus.total_seats):
    #     seat = BusSeat.objects.create(bus=bus,seat_number=i)
    #     seat.save()
    column_one = []
    column_two = []
    column_three = []
    column_four = []

    # Распределяем номера мест по столбцам
    for index, seat in enumerate(bus_seats):
        if index % 4 == 0:
            seat_num = BusSeat.objects.get(bus=bus,seat_number=seat.seat_number)
            column_one.append(seat_num)
        elif index % 4 == 1:
            seat_num = BusSeat.objects.get(bus=bus, seat_number=seat.seat_number)
            column_two.append(seat_num)
        elif index % 4 == 2:
            seat_num = BusSeat.objects.get(bus=bus, seat_number=seat.seat_number)
            column_three.append(seat_num)
        elif index % 4 == 3:
            seat_num = BusSeat.objects.get(bus=bus, seat_number=seat.seat_number)
            column_four.append(seat_num)
    context = {
        'schedule': schedule,
        'bus': bus,
        'title': title,
        'seats': bus_seats,
        'column_one': column_one,
        'column_two': column_two,
        'column_three': column_three,
        'column_four': column_four,
    }

    return render(request, "create_ticket/bus_seats.html", context=context)
