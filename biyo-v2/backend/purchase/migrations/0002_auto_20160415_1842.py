# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='employee_update',
            field=models.ForeignKey(related_name='purchase_updated', verbose_name='Employee that update the order', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
