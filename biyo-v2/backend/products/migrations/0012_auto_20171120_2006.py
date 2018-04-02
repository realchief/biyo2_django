# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_auto_20171108_1437'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalproduct',
            name='print_to',
        ),
        migrations.RemoveField(
            model_name='historicalproduct',
            name='tax_status',
        ),
        migrations.RemoveField(
            model_name='product',
            name='print_to',
        ),
        migrations.RemoveField(
            model_name='product',
            name='tax_status',
        ),
        migrations.AlterField(
            model_name='product',
            name='tax_rate',
            field=models.ForeignKey(related_name='taxrate', verbose_name='Tax Rate', blank=True, to='products.TaxRate', null=True),
            preserve_default=True,
        ),
    ]
