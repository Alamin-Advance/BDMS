# Generated by Django 3.0.8 on 2020-08-04 17:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doner_profile', '0008_auto_20200804_2003'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='Last_Donation_Date_Year_Month_Day',
        ),
    ]
