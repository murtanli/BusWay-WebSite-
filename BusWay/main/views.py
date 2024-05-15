import calendar
import datetime
import locale
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse, Http404, HttpResponseNotFound
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
    bus_seats = BusSeat.objects.filter(schedule=schedule)
    title = 'Выбор места'

    # for i in range(bus.total_seats):
    #     seat = BusSeat.objects.create(bus=bus, schedule=schedule,seat_number=i)
    #     seat.save()

    column_one = []
    column_two = []
    column_three = []
    column_four = []

    # Распределяем номера мест по столбцам
    for index, seat in enumerate(bus_seats):
        if index % 4 == 0:
            seat_num = BusSeat.objects.get(bus=bus,schedule=schedule, seat_number=seat.seat_number)
            column_one.append(seat_num)
        elif index % 4 == 1:
            seat_num = BusSeat.objects.get(bus=bus,schedule=schedule, seat_number=seat.seat_number)
            column_two.append(seat_num)
        elif index % 4 == 2:
            seat_num = BusSeat.objects.get(bus=bus,schedule=schedule, seat_number=seat.seat_number)
            column_three.append(seat_num)
        elif index % 4 == 3:
            seat_num = BusSeat.objects.get(bus=bus,schedule=schedule, seat_number=seat.seat_number)
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


def create_ticket(request):
    title = 'Оформление билета'

    if request.method == 'POST':
        schedule_id = request.POST.get('schedule_id')
        seat_number = request.POST.get('selected_seat')

        profile = Profile.objects.get(user_id=request.user)

        try:
            snils = profile.snils
            email = profile.email
            date_of_birth = profile.date_of_birthday.strftime('%Y-%m-%d')

            user_info = {
                'snils': snils,
                'email': email,
                'date_of_birthday': date_of_birth
            }
        except:
            user_info = {}

        schedule = Schedule.objects.get(id=schedule_id)
        route = schedule.route
        context = {
            'user_info': user_info,
            'title': title,
            'schedule': schedule,
            'route': route,
            'seat_number': seat_number,
        }
        return render(request, 'create_ticket/create_ticket.html', context=context)

    return HttpResponseNotFound(render(request, 'notfound.html'))


def save_ticket(request):
    if request.method == 'POST':
        schedule_id = request.POST.get('schedule_id')
        seat_number = request.POST.get('seat_number')

        snils = request.POST.get('snils')
        date_of_birthday = request.POST.get('date_of_birthday')
        number_phone = request.POST.get('number_phone')
        email = request.POST.get('email')

        user = get_object_or_404(User, id=request.user.id)
        profile = get_object_or_404(Profile, user_id=user.id)

        profile.snils = snils
        profile.date_of_birthday = date_of_birthday
        profile.email = email
        profile.save()

        schedule = Schedule.objects.get(id=schedule_id)
        avalible_seats = schedule.available_seats
        schedule.available_seats = avalible_seats - 1
        schedule.save()

        seat_number = BusSeat.objects.get(bus=schedule.bus,schedule=schedule, seat_number=seat_number)
        seat_number.is_occuiped = True
        seat_number.save()

        Ticket.objects.create(
            profile=profile,
            schedule=schedule,
            sel_seat=seat_number,
            ticket_status='Забронировано'
        )

        return redirect('main_page')
    return HttpResponseNotFound(render(request, 'notfound.html'))


def auth(request):
    if request.method == 'POST':
        login_text = request.POST.get('login')
        password_text = request.POST.get('password')

        user = authenticate(username=login_text, password=password_text)

        if user is not None:
            login(request, user)
            messages.success(request, 'Авторизация прошла успешно!')
            return redirect('main_page')
        else:
            messages.error(request, 'Ошибка авторизации, неправильно введен пароль либо логин')
            return redirect('main_page')


def sign_up(request):
    message = ""
    if request.method == 'POST':
        login_text = request.POST.get('login')
        password_text = request.POST.get('password')

        try:
            user = User.objects.create_user(username=login_text, password=password_text)
            profile = Profile.objects.create(user_id=user)
            profile.save()
            messages.success(request, 'Регистрация прошла успешно!')
        except:
            messages.error(request,
                           'Ошибка регистрации. Пользователь с таким логином уже существует или произошла ошибка при заполнении формы.')

        return redirect('main_page')
    else:
        return redirect('main_page')


def profile_view(request):
    if request.user.is_authenticated:
        user = request.user
        profile = Profile.objects.get(user_id=request.user)
        tickets = Ticket.objects.filter(profile=profile)

        title_name = 'Профиль'
        locale.setlocale(locale.LC_ALL, 'Russian_Russia.utf8')
        today = datetime.today()
        formatted_date = today.strftime('%d %B %Y')

        today = timezone.now()

        context = {
            'title': title_name,
            'user': user,
            'profile': profile,
            'tickets': tickets,
            'today': formatted_date
        }

        return render(request, 'profile_page/profile.html', context=context)

    return HttpResponseNotFound(render(request, 'notfound.html'))

def delete_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)

    seat = BusSeat.objects.get(id=ticket.sel_seat.id)
    seat.is_occuiped = False
    seat.save()

    schedule = Schedule.objects.get(id=ticket.schedule.id)
    av_seats = schedule.available_seats
    schedule.available_seats = av_seats + 1
    schedule.save()

    ticket.delete()

    return redirect('profile_view')


