# Generated by Django 4.1.4 on 2022-12-31 08:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_rename_location_profile_city_profile_address_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderplaced',
            old_name='customer',
            new_name='profile',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='id_user',
        ),
        migrations.AlterField(
            model_name='profile',
            name='birth_date',
            field=models.DateField(default=datetime.date(2022, 12, 31)),
        ),
    ]