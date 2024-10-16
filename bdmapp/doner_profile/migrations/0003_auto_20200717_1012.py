# Generated by Django 3.0.8 on 2020-07-17 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doner_profile', '0002_profile_profile_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='location',
        ),
        migrations.AddField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=12),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, default='IMG_20200309_064310.jpg', null=True, upload_to='users/'),
        ),
    ]
