# -*- coding: utf-8 -*-
import datetime
import re

from django.db import models
from django.db.models import Sum
from django.template import Library
from django.template.defaultfilters import stringfilter
from django.core.urlresolvers import reverse
from django.views.decorators.cache import cache_page

from products.models import Terminal, Product
register = Library()


@register.filter
def field_verbose_name(obj, field_name):
    assert isinstance(obj, models.Model), '%s should be a model instance' % obj

    try:
        value = obj._meta.model._meta.get_field_by_name(field_name)[0].verbose_name
        return value if isinstance(value, basestring) else unicode(value)
    except IndexError:
        return ''


@cache_page(3600 * 15)
@register.assignment_tag
def terminal_tablets_exists():
    if Terminal.objects.filter(mode=1).count() > 0:
        return True
    else:
        return False


@register.filter
def field_value(obj, field_name):
    assert isinstance(obj, models.Model), '%s should be a model instance' % obj

    field = obj._meta.model._meta.get_field_by_name(field_name)[0]
    value = getattr(obj, field_name)

    if field.choices:
        for row in field.choices:
            if value == row[0]:
                return row[1]
        return 'Choice not found'

    elif isinstance(field, models.ManyToManyField):
        return ', '.join(
            [row.__unicode__() for row in getattr(obj, field_name).all()]
        )

    return value


@register.filter
def print_timestamp(timestamp):
    try:
        # assume, that timestamp is given in seconds with decimal point
        ts = float(timestamp)
    except ValueError:
        return None
    except TypeError:
        return None
    return datetime.datetime.fromtimestamp(ts)


@register.filter
def subtotal(order_item):
    return (order_item.price + reduce(lambda x, y: x + y.price, order_item.get_modifiers(), 0.0) - order_item.discount)\
        * order_item.quantity


@register.filter
def urldateperiod(self, url):
    # tz = Store.objects.get(pk=1).timezone
    # tz = pytz.timezone(tz)
    # fmt_start = '%B%d,%Y12:00AM'
    # fmt_end = '%B%d,%Y11:59PM'
    # utc = pytz.utc
    # utc_dt = utc.localize(datetime.datetime.now())
    # local_dt = tz.normalize(utc_dt.astimezone(tz))
    # start = local_dt.strftime(fmt_start)
    # end = local_dt.strftime(fmt_end)
    # return self+'?start='+str(start)+'&end='+str(end)+'&option=0'
    return self + url


@register.filter
def groups_ids(groups):
    ids = groups.all().values_list('id', flat=True)
    return ','.join([str(id) for id in ids])


@register.filter
def get_tips(payments):
    return payments.aggregate(Sum('tips'))['tips__sum']


@register.filter
def dodeduction(value1, value2):
    return value1 - value2


@register.filter
def dopluss(value1, value2):
    return value1 + value2


@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()


@register.filter
def get_current_date_period_from_url(self, current_date):
    return self + current_date


@register.filter
def in_category(special_prices_all, productid):
    product = Product.objects.get(pk=productid)
    if product:
        return special_prices_all.filter(product=product)
    else:
        return False


@register.filter(name='lookup')
def cut(value, arg):
    obj = value[arg]
    cat = []
    if obj['parent']:
        cat.append((obj['sales'], obj['categories']))

    return cat


@register.filter(name='check_in')
def check_in_list_category_pages(value):
    list = ('item_sales',
            'discount_summary',
            'accountant_summary',
            'hourly_sales',
            'order_gross_profit',
            'employee_sales_summary',
            'sales_summary',
            'employee_hour_summary',
            'time_card_weekly',
            'order_types',
            'top_customers',
            'payouts_orders',
            'item_sales_pdf',
            'sales_summary_pdf',
            'price_adjustment')
    if value in list:
        return True
    return False


@register.filter
@stringfilter
def product_order_link(string):
    if "rder #" in string:
        oi_re = re.compile(r'order \#\s?(\d+)', re.I)
        mtch = oi_re.search(string)
        if mtch:
            newstr = '<a href="%s">%s</a>' % (reverse('order-detail', kwargs={'pk': mtch.groups()[0]}), mtch.group())
            string = string.replace(mtch.group(), newstr)
    return string


@register.filter
@stringfilter
def fix_langcode(lang):
    # to deal with 'web-icons' package
    if lang == 'en':
        return 'us'
    return lang
