# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0003_auto_20160217_2041'),
    ]

    operations = [
        migrations.CreateModel(
            name='CsvCustomer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group_csv', models.FileField(upload_to=b'csv')),
                ('created', models.DateTimeField(editable=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
