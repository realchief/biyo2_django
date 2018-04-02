# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0002_auto_20160415_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseitem',
            name='purchase',
            field=models.ForeignKey(related_name='purchase_items', verbose_name='Purchase', to='purchase.Purchase'),
            preserve_default=True,
        ),
    ]
