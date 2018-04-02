# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import terminalapi.models


class Migration(migrations.Migration):

    dependencies = [
        ('terminalapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectversion',
            name='installer',
            field=models.FileField(storage=terminalapi.models.upload_to, upload_to=terminalapi.models.upload_to_f),
            preserve_default=True,
        ),
    ]
