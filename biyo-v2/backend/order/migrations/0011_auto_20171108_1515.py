# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0010_auto_20171108_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='create_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 8, 15, 15, 38, 166192), null=True, blank=True),
            preserve_default=True,
        ),
    ]
