from django.contrib import admin

# Register your models here.
from app import models

admin.site.register(models.Student)

admin.site.register(models.Parent)

admin.site.register(models.Hostel)

admin.site.register(models.Food)
admin.site.register(models.Warden)

admin.site.register(models.Notifications)
admin.site.register(models.BookRoom)