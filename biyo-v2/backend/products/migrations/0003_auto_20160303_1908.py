# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_historicalproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalproduct',
            name='change_reason',
            field=models.CharField(default=b'', max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicalproduct',
            name='stock_change',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='change_reason',
            field=models.CharField(default=b'', max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='stock_change',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
