# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0005_supplier'),
        ('products', '0003_auto_20160303_1908'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='suppliers',
            field=models.ManyToManyField(related_name='suppliers', null=True, to='employees.Supplier', blank=True),
            preserve_default=True,
        ),
    ]
