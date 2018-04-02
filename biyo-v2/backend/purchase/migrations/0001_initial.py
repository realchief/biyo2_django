# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_suppliers'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('document_number', models.CharField(max_length=200, null=True, verbose_name='Document number')),
                ('status', models.CharField(default=b'draft', max_length=10, verbose_name='Status', choices=[(b'draft', 'Draft'), (b'shipped', 'Shipped'), (b'accepted', 'Accepted'), (b'deleted', 'Deleted')])),
                ('note', models.TextField(verbose_name='Note')),
                ('shipped_dt', models.DateTimeField(null=True, verbose_name='Shipped date')),
                ('accepted_dt', models.DateTimeField(null=True, verbose_name='Accepted date')),
                ('created_dt', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('employee_created', models.ForeignKey(related_name='purchase_created', verbose_name='Employee that created the order', to=settings.AUTH_USER_MODEL)),
                ('employee_update', models.ForeignKey(related_name='purchase_updated', verbose_name='Employee that update the order', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PurchaseItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entered_stock', models.DecimalField(verbose_name='Entered stock', max_digits=20, decimal_places=2)),
                ('accepted_stock', models.DecimalField(null=True, verbose_name='Accepted stock', max_digits=20, decimal_places=2)),
                ('difference_stock', models.DecimalField(null=True, verbose_name='Difference stock', max_digits=20, decimal_places=2)),
                ('current_stock', models.DecimalField(null=True, verbose_name='Current stock', max_digits=20, decimal_places=2)),
                ('scan_dt', models.DateTimeField(null=True, verbose_name='Scan date')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Is deleted')),
                ('product', models.ForeignKey(verbose_name='Product', to='products.Product', null=True)),
                ('purchase', models.ForeignKey(verbose_name='Purchase', to='purchase.Purchase')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
