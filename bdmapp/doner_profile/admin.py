from django.contrib import admin

from .models import Profile

class ProfileModel(admin.ModelAdmin):
    list_display = ["__str__", "added","updated"]
    search_fields =  ["__str__", "details"]
    list_filter = ["added","updated"]
    class Meta:
        Model=Profile
admin.site.register(Profile, ProfileModel) 