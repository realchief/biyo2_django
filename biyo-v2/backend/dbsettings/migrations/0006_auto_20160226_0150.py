# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dbsettings', '0005_auto_20160226_0144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dbsettings',
            name='name',
            field=models.CharField(default='', max_length=50, verbose_name='Name'),
            preserve_default=False,
        ),
    ]
