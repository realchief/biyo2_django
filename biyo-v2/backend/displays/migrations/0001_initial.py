# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Box',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('row', models.IntegerField()),
                ('col', models.IntegerField()),
                ('size_x', models.IntegerField()),
                ('size_y', models.IntegerField()),
                ('background_color', models.CharField(max_length=7)),
                ('archived', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Display',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('background_color', models.CharField(max_length=7)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Element',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.IntegerField(choices=[(1, b'IMAGE'), (2, b'CATEGORY'), (3, b'PRODUCT'), (4, b'TWITTER'), (5, b'INSTAGRAM'), (6, b'FACEBOOK'), (7, b'FOURSQUARE'), (8, b'YELP'), (9, b'IMAGES'), (10, b'WEATHER')])),
                ('value', models.CharField(max_length=128)),
                ('archived', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('display', models.ForeignKey(related_name='pages', to='displays.Display')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.ImageField(upload_to=b'pictures')),
                ('slug', models.SlugField(blank=True)),
                ('box', models.ForeignKey(related_name='box_images', blank=True, to='displays.Box', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='box',
            name='display',
            field=models.ForeignKey(related_name='boxes', to='displays.Display'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='box',
            name='element',
            field=models.OneToOneField(null=True, blank=True, to='displays.Element'),
            preserve_default=True,
        ),
    ]
