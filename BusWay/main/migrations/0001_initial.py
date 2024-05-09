# Generated by Django 5.0.6 on 2024-05-09 23:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=100)),
                ('total_seats', models.IntegerField(max_length=30)),
                ('license_plate', models.CharField(max_length=9)),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin', models.CharField(max_length=30)),
                ('destination', models.CharField(max_length=30)),
                ('departure_time', models.DateTimeField()),
                ('arrival_time', models.DateTimeField()),
                ('duration', models.IntegerField(max_length=20)),
                ('distance', models.IntegerField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='BusSeat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_number', models.IntegerField(max_length=30)),
                ('is_occuiped', models.BooleanField(default=False)),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.bus')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=30)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available_seats', models.IntegerField(max_length=30)),
                ('price', models.IntegerField(max_length=30)),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.bus')),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.route')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_status', models.CharField(choices=[('Забронировано', 'Забронировано'), ('Ждет оплаты', 'Ждет оплаты'), ('Оплачен', 'Оплачен')], max_length=30)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.profile')),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.schedule')),
                ('sel_seat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.busseat')),
            ],
        ),
    ]