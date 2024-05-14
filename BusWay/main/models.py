from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=30 , null=True, blank=True)
    email = models.EmailField(max_length=30, default="Empty")
    number_phone = models.CharField(max_length=11, default="Empty")
    date_of_birthday = models.DateField(null=True, blank=True)
class Bus(models.Model):
    brand = models.CharField(max_length=100)
    total_seats = models.IntegerField()
    license_plate = models.CharField(max_length=9)

class BusSeat(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    seat_number = models.IntegerField()
    is_occuiped = models.BooleanField(default=False)

class Route(models.Model):
    origin = models.CharField(max_length=30)
    destination = models.CharField(max_length=30)
    origin_address = models.CharField(max_length=50, default='Empty')
    destination_address = models.CharField(max_length=50, default='Empty')
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    duration = models.IntegerField()
    distance = models.IntegerField()

class Schedule(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    available_seats = models.IntegerField()
    price = models.IntegerField()

class Ticket(models.Model):
    status = (
        ('Забронировано', 'Забронировано'),
        ('Ждет оплаты', 'Ждет оплаты'),
        ('Оплачен', 'Оплачен')
    )
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    sel_seat = models.ForeignKey(BusSeat, on_delete=models.CASCADE)
    ticket_status = models.CharField(choices=status, max_length=30)
