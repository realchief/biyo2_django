# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_auto_20161207_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='create_at',
            field=models.DateTimeField(default=datetime.datetime.now, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='terminal_id',
            field=models.IntegerField(default=-1, null=True, blank=True),
            preserve_default=True,
        ),
    ]
