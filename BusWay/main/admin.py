import locale

from django.contrib import admin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import *
from datetime import time
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'snils', 'email', 'date_of_birthday', 'user_login')
    list_display_links = ('pk', 'user_login',)

    search_fields = ('user_id__username', 'email', 'snils')
    def user_login(self, obj):
        return obj.user_id.username

    user_login.short_description = 'User Login'

@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ('pk', 'brand', 'total_seats', 'license_plate')
    search_fields = ('brand', 'license_plate')


class TimeFilter(admin.SimpleListFilter):
    title = 'Time'
    parameter_name = 'time'

    def lookups(self, request, model_admin):
        return [
            ('morning', 'Утро (06:00 - 12:00)'),
            ('afternoon', 'День (12:00 - 18:00)'),
            ('evening', 'Вечер (18:00 - 00:00)'),
            ('night', 'Ночь (00:00 - 06:00)'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'morning':
            return queryset.filter(schedule__route__departure_time__time__range=(time(6, 0), time(11, 59)))
        if self.value() == 'afternoon':
            return queryset.filter(schedule__route__departure_time__time__range=(time(12, 0), time(17, 59)))
        if self.value() == 'evening':
            return queryset.filter(schedule__route__departure_time__time__range=(time(18, 0), time(23, 59)))
        if self.value() == 'night':
            return queryset.filter(schedule__route__departure_time__time__range=(time(0, 0), time(5, 59)))
        return queryset


@admin.register(BusSeat)
class BusSeatAdmin(admin.ModelAdmin):
    list_display = ('pk', 'schedule_inf', 'seat_number', 'is_occuiped', 'bus_license_plate')
    list_display_links = ('pk', 'bus_license_plate',)
    search_fields = ('bus__brand', 'schedule__route__origin', 'schedule__route__destination')
    list_filter = (TimeFilter,)

    def bus_license_plate(self, obj):
        return obj.bus.license_plate

    bus_license_plate.short_description = 'License plate'

    def schedule_inf(self, obj):
        depart_time = obj.schedule.route.departure_time
        arriv_time = obj.schedule.route.arrival_time

        locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
        depart_time_formatted = depart_time.strftime('%d %B %Y %H:%M')
        arriv_time_formatted = arriv_time.strftime('%d %B %Y %H:%M')

        return f"{obj.schedule.route.origin} - {obj.schedule.route.destination} {depart_time_formatted} - {arriv_time_formatted}"

    schedule_inf.short_description = 'Schedule Information'
class RouteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'origin', 'origin_address', 'destination', 'destination_address', 'departure_time', 'arrival_time', 'duration', 'distance')
    search_fields = ('origin', 'destination')
    list_filter = ('departure_time', 'arrival_time',)
@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'route_name', 'license_plate_bus', 'available_seats', 'price')
    list_display_links = ('route_name', 'license_plate_bus',)
    list_filter = ('route__departure_time', 'available_seats')
    search_fields = ('route__origin', 'route__destination')

    def route_name(self, obj):
        return f"{obj.route.origin} - {obj.route.destination}"

    route_name.short_description = "Route name"

    def license_plate_bus(self, obj):
        return obj.bus.license_plate

    license_plate_bus.short_description = "License plate"
@receiver(post_save, sender=Schedule)
def create_bus_seats(sender, instance, created, **kwargs):
    if created:
        bus = instance.bus
        total_seats = bus.total_seats
        for seat_number in range(1, total_seats + 1):
            BusSeat.objects.create(
                bus=bus,
                schedule=instance,
                seat_number=seat_number
            )

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('pk', 'profile', 'schedule_route', 'selected_seat', 'ticket_status')
    list_display_links = ('profile', 'schedule_route', 'selected_seat')
    search_fields = ('profile__user_id__username', 'schedule__route__origin', 'schedule__route__destination')




    def schedule_route(self, obj):
        route = obj.schedule.route
        return f"{route.origin} - {route.destination}"

    schedule_route.short_description = "Schedule route"

    def selected_seat(self, obj):
        return f"{obj.sel_seat.bus.license_plate} - {obj.sel_seat.seat_number}"

    selected_seat.short_description = "Selected seat"