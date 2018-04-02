# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20161201_1044'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalproduct',
            name='small_image',
            field=models.TextField(max_length=100, null=True, verbose_name='Image', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='small_image',
            field=models.ImageField(upload_to=b'product_images/', null=True, verbose_name='Image', blank=True),
            preserve_default=True,
        ),
    ]
