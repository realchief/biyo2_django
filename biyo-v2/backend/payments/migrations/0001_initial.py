# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
        ('order', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.FloatField()),
                ('amount_paid', models.FloatField(null=True)),
                ('tips', models.FloatField(null=True, blank=True)),
                ('change_amount', models.FloatField()),
                ('card_lastfour', models.CharField(max_length=4, null=True, blank=True)),
                ('payment_type', models.CharField(max_length=255)),
                ('payment_date', models.DateTimeField()),
                ('payment_form', models.CharField(max_length=64, null=True, blank=True)),
                ('authorization', models.CharField(max_length=64, null=True, blank=True)),
                ('transaction_type', models.IntegerField(choices=[(1, b'Sale'), (2, b'Void'), (3, b'Return')])),
                ('processor_response', models.CharField(max_length=100)),
                ('batch_num', models.CharField(max_length=100, null=True, blank=True)),
                ('approval_code', models.IntegerField(null=True, blank=True)),
                ('transaction_id', models.CharField(max_length=100, null=True, blank=True)),
                ('terminal_id', models.IntegerField(null=True, blank=True)),
                ('signature', models.TextField(null=True, blank=True)),
                ('void_ref', models.IntegerField(null=True, blank=True)),
                ('employee', models.ForeignKey(related_name='payments_accepted', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('order', models.ForeignKey(related_name='payments', to='order.Order')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Payout',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('payout_type', models.CharField(max_length=7, choices=[(b'IN', b'IN'), (b'OUT', b'OUT'), (b'DEPOSIT', b'DEPOSIT')])),
                ('payout_value', models.FloatField(default=0.0, null=True, blank=True)),
                ('payout_time', models.DateTimeField(null=True, blank=True)),
                ('payout_note', models.CharField(default=b'', max_length=100, null=True, blank=True)),
                ('employee', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('shift_open_date', models.DateTimeField(auto_now_add=True)),
                ('shift_update_date', models.DateTimeField(auto_now=True)),
                ('shift_close_date', models.DateTimeField(null=True, blank=True)),
                ('opening_amount', models.FloatField(default=0.0, null=True, blank=True)),
                ('total_cashtenders', models.FloatField(default=0.0, null=True, blank=True)),
                ('total_cashreturns', models.FloatField(default=0.0, null=True, blank=True)),
                ('total_drops', models.FloatField(default=0.0, null=True, blank=True)),
                ('total_payouts', models.FloatField(default=0.0, null=True, blank=True)),
                ('closing_amount', models.FloatField(default=0.0, null=True, blank=True)),
                ('over_shortage', models.FloatField(default=0.0, null=True, blank=True)),
                ('close_shift_employee', models.ForeignKey(related_name='employee_closed', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('open_shift_employee', models.ForeignKey(related_name='employee_opened', to=settings.AUTH_USER_MODEL)),
                ('terminal', models.ForeignKey(related_name='shift_terminal', to='products.Terminal')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='payout',
            name='shift',
            field=models.ForeignKey(related_name='shift_payouts', blank=True, to='payments.Shift', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='payout',
            name='terminal',
            field=models.ForeignKey(to='products.Terminal'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='payment',
            name='shift',
            field=models.ForeignKey(blank=True, to='payments.Shift', null=True),
            preserve_default=True,
        ),
    ]
