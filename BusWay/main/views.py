import datetime
import locale

from django.contrib.auth import logout
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import *

def main_page(request):
    routes = []
    title_name = 'Главная страница'
    locale.setlocale(locale.LC_ALL, 'Russian_Russia.utf8')
    today = datetime.date.today()
    formatted_date = today.strftime('%d %B %Y')

    today = timezone.now()
    upcoming_routes = Route.objects.filter(departure_time__gt=today)
    for route in upcoming_routes:
        schedule = Schedule.objects.filter(route=route)
        bus = ''
        ЧУЙ МОРЖА
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
    pass