# Generated by Django 3.0.8 on 2020-07-18 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doner_profile', '0004_auto_20200718_1420'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='Last_Donation_Date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='Phone_Number',
            field=models.CharField(blank=True, max_length=11),
        ),
    ]
