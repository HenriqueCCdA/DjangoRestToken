from django.contrib import admin

from api.core.models import CustomUser, Profile

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Profile)
