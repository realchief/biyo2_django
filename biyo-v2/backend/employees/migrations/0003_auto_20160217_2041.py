# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0002_auto_20160217_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='store',
            field=models.ForeignKey(verbose_name=b'Store', blank=True, to='products.Store', null=True),
            preserve_default=True,
        ),
    ]
