# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0004_csvcustomer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('supplier', models.CharField(max_length=32, verbose_name='Supplier Name')),
                ('default_markup', models.PositiveIntegerField(default=0, verbose_name='Default Markup')),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('company', models.CharField(max_length=32, verbose_name='Company')),
                ('first_name', models.CharField(max_length=32, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=32, verbose_name='Last Name')),
                ('archived', models.BooleanField(default=False)),
                ('created', models.DateTimeField(editable=False)),
                ('phone', models.CharField(max_length=60, null=True, verbose_name='Phone', blank=True)),
                ('mobile', models.CharField(max_length=60, null=True, verbose_name='Mobile Phone', blank=True)),
                ('fax', models.CharField(max_length=60, null=True, verbose_name='Fax', blank=True)),
                ('email', models.EmailField(unique=True, max_length=75, verbose_name='Email')),
                ('website', models.URLField(null=True, verbose_name='Website', blank=True)),
                ('street', models.CharField(max_length=32, null=True, verbose_name='Street', blank=True)),
                ('suburb', models.CharField(max_length=32, null=True, verbose_name='Suburb', blank=True)),
                ('sity', models.CharField(max_length=32, null=True, verbose_name='Sity', blank=True)),
                ('postcode', models.CharField(max_length=8, null=True, verbose_name='Post Code', blank=True)),
                ('state', models.CharField(blank=True, max_length=2, null=True, verbose_name='State', choices=[(b'AL', 'Alabama'), (b'AK', 'Alaska'), (b'AS', 'American Samoa'), (b'AZ', 'Arizona'), (b'AR', 'Arkansas'), (b'AA', 'Armed Forces Americas'), (b'AE', 'Armed Forces Europe'), (b'AP', 'Armed Forces Pacific'), (b'CA', 'California'), (b'CO', 'Colorado'), (b'CT', 'Connecticut'), (b'DE', 'Delaware'), (b'DC', 'District of Columbia'), (b'FL', 'Florida'), (b'GA', 'Georgia'), (b'GU', 'Guam'), (b'HI', 'Hawaii'), (b'ID', 'Idaho'), (b'IL', 'Illinois'), (b'IN', 'Indiana'), (b'IA', 'Iowa'), (b'KS', 'Kansas'), (b'KY', 'Kentucky'), (b'LA', 'Louisiana'), (b'ME', 'Maine'), (b'MD', 'Maryland'), (b'MA', 'Massachusetts'), (b'MI', 'Michigan'), (b'MN', 'Minnesota'), (b'MS', 'Mississippi'), (b'MO', 'Missouri'), (b'MT', 'Montana'), (b'NE', 'Nebraska'), (b'NV', 'Nevada'), (b'NH', 'New Hampshire'), (b'NJ', 'New Jersey'), (b'NM', 'New Mexico'), (b'NY', 'New York'), (b'NC', 'North Carolina'), (b'ND', 'North Dakota'), (b'MP', 'Northern Mariana Islands'), (b'OH', 'Ohio'), (b'OK', 'Oklahoma'), (b'OR', 'Oregon'), (b'PA', 'Pennsylvania'), (b'PR', 'Puerto Rico'), (b'RI', 'Rhode Island'), (b'SC', 'South Carolina'), (b'SD', 'South Dakota'), (b'TN', 'Tennessee'), (b'TX', 'Texas'), (b'UT', 'Utah'), (b'VT', 'Vermont'), (b'VI', 'Virgin Islands'), (b'VA', 'Virginia'), (b'WA', 'Washington'), (b'WV', 'West Virginia'), (b'WI', 'Wisconsin'), (b'WY', 'Wyoming')])),
                ('country', django_countries.fields.CountryField(max_length=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
