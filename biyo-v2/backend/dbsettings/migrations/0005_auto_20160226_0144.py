# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dbsettings', '0004_auto_20160226_0141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dbsettings',
            name='description',
            field=models.TextField(verbose_name='Description', blank=True),
            preserve_default=True,
        ),
    ]
