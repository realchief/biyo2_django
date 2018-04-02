# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_suppliers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalproduct',
            name='barcode',
            field=models.CharField(max_length=250, null=True, verbose_name='Barcode', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='barcode',
            field=models.CharField(max_length=250, null=True, verbose_name='Barcode', blank=True),
            preserve_default=True,
        ),
    ]
