# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20161202_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to=b'product_images/', null=True, verbose_name='Image', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='small_image',
            field=models.ImageField(upload_to=b'product_images/', width_field=50, height_field=50, blank=True, null=True, verbose_name='Image'),
            preserve_default=True,
        ),
    ]
