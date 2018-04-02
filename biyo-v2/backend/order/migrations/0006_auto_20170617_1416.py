# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_auto_20161208_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='terminal_id',
            field=models.IntegerField(default=-1, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='create_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 17, 14, 16, 15, 21657), null=True, blank=True),
            preserve_default=True,
        ),
    ]
