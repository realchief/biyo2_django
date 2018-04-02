from django.contrib import admin
from . import models


class SettingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'description', 'terminal')
    list_filter = ('name', 'terminal')


admin.site.register(models.DBSettings, SettingsAdmin)
