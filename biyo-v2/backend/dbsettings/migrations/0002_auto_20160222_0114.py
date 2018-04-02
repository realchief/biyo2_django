# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dbsettings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settingnames',
            name='default_value',
            field=models.CharField(max_length=50, null=True, verbose_name='Default value'),
            preserve_default=True,
        ),
    ]
