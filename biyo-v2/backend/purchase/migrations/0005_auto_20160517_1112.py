# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0004_auto_20160426_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='document_number',
            field=models.CharField(max_length=200, null=True, verbose_name='Document number', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='purchase',
            name='note',
            field=models.TextField(null=True, verbose_name='Note', blank=True),
            preserve_default=True,
        ),
    ]
