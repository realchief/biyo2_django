# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(unique=True, max_length=75, verbose_name='Email')),
                ('name', models.CharField(max_length=32, verbose_name='Name')),
                ('address', models.CharField(max_length=32, null=True, verbose_name='Address', blank=True)),
                ('address2', models.CharField(max_length=32, null=True, verbose_name='Address2', blank=True)),
                ('city', models.CharField(max_length=32, null=True, verbose_name='City', blank=True)),
                ('state', models.CharField(blank=True, max_length=2, null=True, verbose_name='State', choices=[(b'AL', 'Alabama'), (b'AK', 'Alaska'), (b'AS', 'American Samoa'), (b'AZ', 'Arizona'), (b'AR', 'Arkansas'), (b'AA', 'Armed Forces Americas'), (b'AE', 'Armed Forces Europe'), (b'AP', 'Armed Forces Pacific'), (b'CA', 'California'), (b'CO', 'Colorado'), (b'CT', 'Connecticut'), (b'DE', 'Delaware'), (b'DC', 'District of Columbia'), (b'FL', 'Florida'), (b'GA', 'Georgia'), (b'GU', 'Guam'), (b'HI', 'Hawaii'), (b'ID', 'Idaho'), (b'IL', 'Illinois'), (b'IN', 'Indiana'), (b'IA', 'Iowa'), (b'KS', 'Kansas'), (b'KY', 'Kentucky'), (b'LA', 'Louisiana'), (b'ME', 'Maine'), (b'MD', 'Maryland'), (b'MA', 'Massachusetts'), (b'MI', 'Michigan'), (b'MN', 'Minnesota'), (b'MS', 'Mississippi'), (b'MO', 'Missouri'), (b'MT', 'Montana'), (b'NE', 'Nebraska'), (b'NV', 'Nevada'), (b'NH', 'New Hampshire'), (b'NJ', 'New Jersey'), (b'NM', 'New Mexico'), (b'NY', 'New York'), (b'NC', 'North Carolina'), (b'ND', 'North Dakota'), (b'MP', 'Northern Mariana Islands'), (b'OH', 'Ohio'), (b'OK', 'Oklahoma'), (b'OR', 'Oregon'), (b'PA', 'Pennsylvania'), (b'PR', 'Puerto Rico'), (b'RI', 'Rhode Island'), (b'SC', 'South Carolina'), (b'SD', 'South Dakota'), (b'TN', 'Tennessee'), (b'TX', 'Texas'), (b'UT', 'Utah'), (b'VT', 'Vermont'), (b'VI', 'Virgin Islands'), (b'VA', 'Virginia'), (b'WA', 'Washington'), (b'WV', 'West Virginia'), (b'WI', 'Wisconsin'), (b'WY', 'Wyoming')])),
                ('zipcode', models.CharField(max_length=8, null=True, verbose_name='Zip code', blank=True)),
                ('phone', models.CharField(max_length=60, null=True, verbose_name='Phone', blank=True)),
                ('pin', models.IntegerField(verbose_name='Pin')),
                ('role', models.IntegerField(verbose_name='Role', choices=[(1, b'Owner'), (2, b'Manager'), (3, b'Cashier'), (4, b'Employee')])),
                ('vein_string', models.TextField(verbose_name='Vein String', blank=True)),
                ('hourly_rate', models.DecimalField(null=True, verbose_name='Hourly Rate', max_digits=5, decimal_places=2, blank=True)),
                ('archived', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('created', models.DateTimeField(editable=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=32)),
                ('last_name', models.CharField(max_length=32)),
                ('email', models.EmailField(max_length=75, null=True, blank=True)),
                ('phone', models.CharField(max_length=32, null=True, blank=True)),
                ('profile_key', models.CharField(max_length=32, null=True, blank=True)),
                ('address', models.CharField(max_length=32, null=True, blank=True)),
                ('rewards_points', models.IntegerField(null=True, blank=True)),
                ('account_number', models.CharField(max_length=64, blank=True)),
                ('notes', models.TextField(null=True, blank=True)),
                ('archived', models.BooleanField(default=False)),
                ('created', models.DateTimeField(editable=False)),
                ('city', models.CharField(max_length=58, null=True, verbose_name='City', blank=True)),
                ('state', models.CharField(blank=True, max_length=2, null=True, verbose_name='State', choices=[(b'AL', 'Alabama'), (b'AK', 'Alaska'), (b'AS', 'American Samoa'), (b'AZ', 'Arizona'), (b'AR', 'Arkansas'), (b'AA', 'Armed Forces Americas'), (b'AE', 'Armed Forces Europe'), (b'AP', 'Armed Forces Pacific'), (b'CA', 'California'), (b'CO', 'Colorado'), (b'CT', 'Connecticut'), (b'DE', 'Delaware'), (b'DC', 'District of Columbia'), (b'FL', 'Florida'), (b'GA', 'Georgia'), (b'GU', 'Guam'), (b'HI', 'Hawaii'), (b'ID', 'Idaho'), (b'IL', 'Illinois'), (b'IN', 'Indiana'), (b'IA', 'Iowa'), (b'KS', 'Kansas'), (b'KY', 'Kentucky'), (b'LA', 'Louisiana'), (b'ME', 'Maine'), (b'MD', 'Maryland'), (b'MA', 'Massachusetts'), (b'MI', 'Michigan'), (b'MN', 'Minnesota'), (b'MS', 'Mississippi'), (b'MO', 'Missouri'), (b'MT', 'Montana'), (b'NE', 'Nebraska'), (b'NV', 'Nevada'), (b'NH', 'New Hampshire'), (b'NJ', 'New Jersey'), (b'NM', 'New Mexico'), (b'NY', 'New York'), (b'NC', 'North Carolina'), (b'ND', 'North Dakota'), (b'MP', 'Northern Mariana Islands'), (b'OH', 'Ohio'), (b'OK', 'Oklahoma'), (b'OR', 'Oregon'), (b'PA', 'Pennsylvania'), (b'PR', 'Puerto Rico'), (b'RI', 'Rhode Island'), (b'SC', 'South Carolina'), (b'SD', 'South Dakota'), (b'TN', 'Tennessee'), (b'TX', 'Texas'), (b'UT', 'Utah'), (b'VT', 'Vermont'), (b'VI', 'Virgin Islands'), (b'VA', 'Virginia'), (b'WA', 'Washington'), (b'WV', 'West Virginia'), (b'WI', 'Wisconsin'), (b'WY', 'Wyoming')])),
                ('zipcode', models.CharField(max_length=8, null=True, verbose_name='Zip code', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TimeClock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_in', models.DateTimeField()),
                ('time_out', models.DateTimeField(null=True)),
                ('archived', models.BooleanField(default=False)),
                ('employee', models.ForeignKey(related_name='time_clock', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
