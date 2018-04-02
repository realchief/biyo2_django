# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SettingNames',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50, verbose_name='Name')),
                ('default_value', models.CharField(max_length=50, verbose_name='Default value')),
            ],
            options={
                'db_table': 'settings_settingnames',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DBSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=50, null=True, verbose_name='Value', blank=True)),
                ('description', models.TextField(verbose_name='Description')),
                ('name', models.ForeignKey(verbose_name='Name', to='dbsettings.SettingNames')),
                ('terminal', models.ForeignKey(verbose_name='Terminal', blank=True, to='products.Terminal', null=True)),
            ],
            options={
                'db_table': 'settings_settings',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='dbsettings',
            unique_together=set([('name', 'terminal')]),
        ),
    ]
