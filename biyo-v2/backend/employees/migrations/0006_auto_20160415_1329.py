# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0005_supplier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='pin',
            field=models.IntegerField(unique=True, verbose_name='Pin'),
            preserve_default=True,
        ),
    ]
