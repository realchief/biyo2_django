# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_original_data_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='sorting',
            field=models.IntegerField(default=0, max_length=255, verbose_name='Sorting'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalproduct',
            name='barcode',
            field=models.CharField(max_length=255, null=True, verbose_name='Barcode', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalproduct',
            name='color',
            field=models.IntegerField(blank=True, max_length=255, null=True, verbose_name='Color', choices=[(1, b'Orange'), (2, b'Aqua'), (3, b'Brown'), (4, b'Green'), (5, b'Cyan'), (6, b'Purple'), (7, b'Pink')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalproduct',
            name='cost',
            field=models.FloatField(default=0.0, max_length=255, null=True, verbose_name='Cost', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalproduct',
            name='price',
            field=models.FloatField(default=0.0, max_length=255, null=True, verbose_name='Price', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalproduct',
            name='price_adjust',
            field=models.IntegerField(default=0, max_length=255, verbose_name='Ask price everytime?', choices=[(1, b'Yes'), (0, b'No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalproduct',
            name='sorting',
            field=models.IntegerField(default=0, max_length=255, null=True, verbose_name='Sorting', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalproduct',
            name='stock',
            field=models.IntegerField(default=0, max_length=255, null=True, verbose_name='Stock', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalproduct',
            name='stock_change',
            field=models.IntegerField(default=0, max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalproduct',
            name='tax_status',
            field=models.IntegerField(default=0, max_length=255, verbose_name='Tax status', choices=[(0, b'Taxed'), (1, b'Not taxed')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='barcode',
            field=models.CharField(max_length=255, null=True, verbose_name='Barcode', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='color',
            field=models.IntegerField(blank=True, max_length=255, null=True, verbose_name='Color', choices=[(1, b'Orange'), (2, b'Aqua'), (3, b'Brown'), (4, b'Green'), (5, b'Cyan'), (6, b'Purple'), (7, b'Pink')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='cost',
            field=models.FloatField(default=0.0, max_length=255, null=True, verbose_name='Cost', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(default=0.0, max_length=255, null=True, verbose_name='Price', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='price_adjust',
            field=models.IntegerField(default=0, max_length=255, verbose_name='Ask price everytime?', choices=[(1, b'Yes'), (0, b'No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='sorting',
            field=models.IntegerField(default=0, max_length=255, null=True, verbose_name='Sorting', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.IntegerField(default=0, max_length=255, null=True, verbose_name='Stock', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='stock_change',
            field=models.IntegerField(default=0, max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='tax_status',
            field=models.IntegerField(default=0, max_length=255, verbose_name='Tax status', choices=[(0, b'Taxed'), (1, b'Not taxed')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reward',
            name='discount',
            field=models.CharField(max_length=250, verbose_name='Reward Type', choices=[(b'Discount', b'Discount'), (b'Text', b'Text')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reward',
            name='discount_type',
            field=models.CharField(max_length=250, verbose_name='Discount Type', choices=[(b'Item', b'Item'), (b'Invoice', b'Invoice')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reward',
            name='discount_type_item',
            field=models.ForeignKey(related_name='product_item', verbose_name='Discount Item', blank=True, to='products.Product', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reward',
            name='points_redeem',
            field=models.IntegerField(null=True, verbose_name='Amount of Points to Redeem'),
            preserve_default=True,
        ),
    ]
