# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0013_auto_20171120_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='create_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 20, 20, 39, 54, 50470), null=True, blank=True),
            preserve_default=True,
        ),
    ]
