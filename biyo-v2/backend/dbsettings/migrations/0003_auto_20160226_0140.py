# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dbsettings', '0002_auto_20160222_0114'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='dbsettings',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='dbsettings',
            name='name',
        ),
        migrations.DeleteModel(
            name='SettingNames',
        )
    ]
