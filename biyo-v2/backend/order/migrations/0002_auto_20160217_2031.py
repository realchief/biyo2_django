# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0001_initial'),
        ('order', '0001_initial'),
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderoption',
            name='product',
            field=models.ForeignKey(related_name='options', to='products.Product'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ordermodifier',
            name='group',
            field=models.ForeignKey(related_name='modifiers_in_orders', to='products.ModifierGroup'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ordermodifier',
            name='item',
            field=models.ForeignKey(related_name='modifiers', to='order.OrderItem'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ordermodifier',
            name='oryginal',
            field=models.ForeignKey(related_name='ordered', to='products.Modifier'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='orderitem',
            name='employee',
            field=models.ForeignKey(related_name='employee_order_items', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(related_name='items', to='order.Order'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(related_name='order_items', blank=True, to='products.Product', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(related_name='orders', blank=True, to='employees.Customer', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='emp_close',
            field=models.ForeignKey(related_name='order_as_close', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='emp_open',
            field=models.ForeignKey(related_name='order_as_open', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='shift',
            field=models.ForeignKey(blank=True, to='payments.Shift', null=True),
            preserve_default=True,
        ),
    ]
