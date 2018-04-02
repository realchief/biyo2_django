# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0007_auto_20160415_1334'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='photo',
            field=models.ImageField(default=b'employee_photo/def.jpg', upload_to=b'employee_photo/', verbose_name='P', blank=True),
            preserve_default=True,
        ),
    ]
