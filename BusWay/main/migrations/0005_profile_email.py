# Generated by Django 5.0.6 on 2024-05-13 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_route_destination_address_route_origin_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.EmailField(default='Empty', max_length=30),
        ),
    ]
