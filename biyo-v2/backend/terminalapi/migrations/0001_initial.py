# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import terminalapi.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectVersion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.CharField(max_length=10)),
                ('installer', models.FileField(storage=terminalapi.models.upload_to, upload_to=b'/storage')),
                ('password', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
