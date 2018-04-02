# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0001_initial'),
        ('auth', '0001_initial'),
        ('taskin', '0001_initial'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='group',
            field=models.ForeignKey(related_name='taskin_group', blank=True, to='taskin.CustomerGroup', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='employee',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='employee',
            name='store',
            field=models.ForeignKey(verbose_name=b'Store', to='products.Store'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='employee',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
            preserve_default=True,
        ),
    ]
