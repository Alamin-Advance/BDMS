from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, date

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Full_Name = models.CharField(max_length=500, blank=False)
    gender=( ('male',"MALE"),('female',"FEMALE"),('other',"OTHER"))
    Gender = models.CharField(max_length=50, choices=gender, blank=False)
    Age = models.CharField(max_length=50, blank=False)
    bg=(('A+',"A+"),('A-',"A-"),('B+',"B+"),('B-',"B-"),('AB+',"AB+"),('AB-',"AB-"),('O+',"O+"),('O-',"O-"))
    Blood_Group = models.CharField(max_length=50, choices=bg, blank=False)
    pro=(('Student',"student"),('Service',"service"),('Job seeker',"job seeker"),('Housewife',"housewife"),('Others',"others"))
    Profession = models.CharField(max_length=50, choices=pro, blank=True)
    Home_District = models.CharField(max_length=50, blank=True)
    Present_Address = models.CharField(max_length=300, blank=False)
    Last_Donation_Date = models.DateField(null=True, blank=True)
    Phone_Number = models.CharField(max_length=11, blank=False)
    Email = models.CharField(max_length=300, blank=True)
    Profile_Image = models.ImageField(default='800px-Blood_donation_pictogram.svg.png', upload_to='users/', null=True, blank=True)    
    added = models.DateTimeField( auto_now=False, auto_now_add=True)
    updated = models.DateTimeField( auto_now=True, auto_now_add=False)

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()