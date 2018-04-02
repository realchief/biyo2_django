# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_auto_20161202_1108'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalproduct',
            name='small_image',
        ),
        migrations.RemoveField(
            model_name='product',
            name='small_image',
        ),
        migrations.AddField(
            model_name='historicalproduct',
            name='description',
            field=models.CharField(max_length=224, null=True, verbose_name=b'Description', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.CharField(max_length=224, null=True, verbose_name=b'Description', blank=True),
            preserve_default=True,
        ),
    ]
