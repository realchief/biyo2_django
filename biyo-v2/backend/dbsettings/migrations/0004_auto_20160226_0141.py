# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dbsettings', '0003_auto_20160226_0140'),
    ]

    operations = [
        migrations.AddField(
            model_name='dbsettings',
            name='name',
            field=models.CharField(max_length=50, null=True, verbose_name='Name', blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='dbsettings',
            unique_together=set([('name', 'terminal')]),
        ),
    ]
