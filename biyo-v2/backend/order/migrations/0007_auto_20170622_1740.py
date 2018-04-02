# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_auto_20170617_1416'),
    ]

    operations = [
        migrations.CreateModel(
            name='SharedOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.CharField(default=uuid.uuid4, max_length=512)),
                ('order', models.ForeignKey(to='order.Order')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='create_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 22, 17, 40, 22, 333608), null=True, blank=True),
            preserve_default=True,
        ),
    ]
