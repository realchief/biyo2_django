# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=32)),
                ('subtotal', models.FloatField()),
                ('tax_total', models.FloatField()),
                ('discount_total', models.FloatField()),
                ('grand_total', models.FloatField()),
                ('balance_remaining', models.FloatField(null=True, blank=True)),
                ('open_date', models.DateTimeField(null=True, blank=True)),
                ('hold_date', models.DateTimeField(null=True, blank=True)),
                ('close_date', models.DateTimeField(null=True, blank=True)),
                ('status', models.IntegerField(choices=[(1, b'Open'), (2, b'Hold'), (3, b'Closed'), (4, b'Canceled'), (5, b'Refunded')])),
                ('description', models.CharField(max_length=128, null=True, blank=True)),
                ('discount_orders', models.FloatField(null=True, blank=True)),
                ('terminal_id', models.IntegerField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('price', models.FloatField()),
                ('cost', models.FloatField()),
                ('discount', models.FloatField()),
                ('tax', models.FloatField()),
                ('void_status', models.IntegerField(null=True, blank=True)),
                ('quantity', models.IntegerField()),
                ('terminal_id', models.IntegerField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderModifier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('cost', models.FloatField()),
                ('price', models.FloatField()),
                ('void_status', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('cost', models.FloatField()),
                ('price', models.FloatField()),
                ('item', models.ForeignKey(related_name='options', to='order.OrderItem')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
