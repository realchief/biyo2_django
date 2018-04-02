# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_auto_20170622_1740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='create_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 3, 17, 0, 33, 776076), null=True, blank=True),
            preserve_default=True,
        ),
    ]
