# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_auto_20171120_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalproduct',
            name='price_adjust',
            field=models.BooleanField(default=False, verbose_name='Ask price everytime?', choices=[(True, b'Yes'), (False, b'No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='price_adjust',
            field=models.BooleanField(default=False, verbose_name='Ask price everytime?', choices=[(True, b'Yes'), (False, b'No')]),
            preserve_default=True,
        ),
    ]
