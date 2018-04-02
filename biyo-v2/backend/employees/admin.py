from django.contrib import admin
from . import models

admin.site.register(models.Employee)
admin.site.register(models.Customer)
admin.site.register(models.Supplier)
admin.site.register(models.TimeClock)
