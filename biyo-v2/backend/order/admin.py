import datetime

from django.contrib import admin

from order.models import Order
from . import models

# admin.site.register(models.Order)
admin.site.register(models.OrderItem)
admin.site.register(models.OrderModifier)
admin.site.register(models.OrderOption)


def make_published(self, request, queryset):
    rows_updated = queryset.update(status=3, close_date=datetime.datetime.now())
    if rows_updated == 1:
        message_bit = "1 order was"
    else:
        message_bit = "%s orders were" % rows_updated
        self.message_user(request, "%s successfully marked as closed." % message_bit)


make_published.short_description = "Mark selected orders as closed"


def case_name(obj):
    return ("Order # %s" % (obj.id,))


case_name.short_description = 'Name'


class OrderAdmin(admin.ModelAdmin):
    list_display = (case_name, 'status')
    # ordering = ['id']
    actions = [make_published]


admin.site.register(Order, OrderAdmin)
