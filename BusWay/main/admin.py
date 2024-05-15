from django.contrib import admin
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import *

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'snils', 'email', 'date_of_birthday', 'user_login')
    list_display_links = ('pk', 'user_login',)

    def user_login(self, obj):
        return obj.user_id.username

    user_login.short_description = 'User Login'

@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ('pk', 'brand', 'total_seats', 'license_plate')

@admin.register(BusSeat)
class BusSeatAdmin(admin.ModelAdmin):
    list_display = ('pk','schedule', 'seat_number', 'is_occuiped', 'bus_license_plate')
    list_display_links = ('pk', 'bus_license_plate',)

    def bus_license_plate(self, obj):
        return obj.bus.license_plate

    bus_license_plate.short_description = 'License plate'

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'origin', 'origin_address', 'destination', 'destination_address', 'departure_time', 'arrival_time', 'duration', 'distance')

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'route_name', 'license_plate_bus', 'available_seats', 'price')
    list_display_links = ('route_name', 'license_plate_bus',)

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
    list_display = ('pk', 'user_full_name', 'schedule_route', 'selected_seat', 'ticket_status')
    list_display_links = ('user_full_name', 'schedule_route', 'selected_seat')

    def user_full_name(self, obj):
        return f"{obj.profile.first_name} {obj.profile.last_name}"

    user_full_name.short_description = "User full name"

    def schedule_route(self, obj):
        route = obj.schedule.route
        return f"{route.origin} - {route.destination}"

    schedule_route.short_description = "Schedule route"

    def selected_seat(self, obj):
        return f"{obj.sel_seat.bus.license_plate} - {obj.sel_seat.seat_number}"

    selected_seat.short_description = "Selected seat"