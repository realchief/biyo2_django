# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0008_employee_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supplier',
            name='sity',
        ),
        migrations.AddField(
            model_name='supplier',
            name='city',
            field=models.CharField(max_length=32, null=True, verbose_name='City', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='supplier',
            name='default_markup',
            field=models.PositiveIntegerField(default=0, max_length=255, verbose_name='Default Markup'),
            preserve_default=True,
        ),
    ]
