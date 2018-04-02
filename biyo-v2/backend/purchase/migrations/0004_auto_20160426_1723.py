# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0003_auto_20160415_2017'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchaseitem',
            name='current_stock',
        ),
        migrations.RemoveField(
            model_name='purchaseitem',
            name='difference_stock',
        ),
    ]
