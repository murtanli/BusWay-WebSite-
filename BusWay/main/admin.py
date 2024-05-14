from django.contrib import admin
from .models import *

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('pk','first_name', 'last_name', 'email', 'date_of_birthday', 'number_phone', 'user_login')
    list_display_links = ('user_login',)

    def user_login(self, obj):
        return obj.user_id.username

    user_login.short_description = 'User Login'

@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ('pk', 'brand', 'total_seats', 'license_plate')

@admin.register(BusSeat)
class BusSeatAdmin(admin.ModelAdmin):
    list_display = ('pk', 'seat_number', 'is_occuiped', 'bus_license_plate')
    list_display_links = ('bus_license_plate',)

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