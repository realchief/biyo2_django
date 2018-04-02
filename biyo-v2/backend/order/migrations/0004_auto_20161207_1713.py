# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20160326_0100'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='create_at',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='orderitem',
            name='voided_at',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
