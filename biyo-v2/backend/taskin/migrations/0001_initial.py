# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=125, verbose_name='Group Name')),
                ('archived', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SpecialPrices',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.FloatField(verbose_name='Price')),
                ('archived', models.BooleanField(default=False)),
                ('group', models.ForeignKey(related_name='taskin_special_price_group', to='taskin.CustomerGroup')),
                ('product', models.ForeignKey(related_name='special_prices_items', to='products.Product')),
            ],
            options={
                'ordering': ['price'],
            },
            bases=(models.Model,),
        ),
    ]
