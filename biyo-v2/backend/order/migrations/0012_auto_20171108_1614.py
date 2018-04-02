# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0011_auto_20171108_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='create_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 8, 16, 14, 33, 910447), null=True, blank=True),
            preserve_default=True,
        ),
    ]
