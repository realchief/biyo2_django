# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0006_auto_20160415_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='pin',
            field=models.IntegerField(unique=True, null=True, verbose_name='Pin'),
            preserve_default=True,
        ),
    ]
