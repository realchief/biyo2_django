# -*- coding: utf-8 -*-
from django.template import Library


register = Library()


@register.filter
def sum_price(qs):
    return sum((x.price for x in qs))


@register.filter
def sum_taxes(qs):
    return sum((x.tax for x in qs))


@register.filter
def dodeduction(value1, value2):
    return value1 - value2
