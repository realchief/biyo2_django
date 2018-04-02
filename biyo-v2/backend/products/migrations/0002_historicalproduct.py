# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalProduct',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('name', models.CharField(max_length=64, verbose_name='Name')),
                ('image', models.TextField(max_length=100, null=True, verbose_name='Image', blank=True)),
                ('color', models.IntegerField(blank=True, null=True, verbose_name='Color', choices=[(1, b'Orange'), (2, b'Aqua'), (3, b'Brown'), (4, b'Green'), (5, b'Cyan'), (6, b'Purple'), (7, b'Pink')])),
                ('sorting', models.IntegerField(default=0, null=True, verbose_name='Sorting', blank=True)),
                ('cost', models.FloatField(default=0.0, null=True, verbose_name='Cost', blank=True)),
                ('price', models.FloatField(default=0.0, null=True, verbose_name='Price', blank=True)),
                ('barcode', models.CharField(default=0.0, max_length=250, null=True, verbose_name='Barcode', blank=True)),
                ('stock', models.IntegerField(default=0, null=True, verbose_name='Stock', blank=True)),
                ('tax_status', models.IntegerField(default=0, verbose_name='Tax status', choices=[(0, b'Taxed'), (1, b'Not taxed')])),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('archived', models.BooleanField(default=False)),
                ('price_adjust', models.IntegerField(default=0, verbose_name='Ask price everytime?', choices=[(1, b'Yes'), (0, b'No')])),
                ('print_to', models.BooleanField(default=False, verbose_name='Print to Kitchen', choices=[(True, b'Yes'), (False, b'No')])),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('printer', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='products.Printer', null=True)),
                ('tax_rate', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='products.TaxRate', null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical product',
            },
            bases=(models.Model,),
        ),
    ]
