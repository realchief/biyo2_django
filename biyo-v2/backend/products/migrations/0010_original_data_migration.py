# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_auto_20161207_1348'),
    ]

    operations = [
        migrations.RunSQL("""
             insert into products_taxrate (archived, name, rate) values (0, 'NY Tax Rate', 8);

             insert into products_product
             (id, tax_rate_id, description, stock_change, active,
             price_adjust, change_reason, printer_id,
             tax_status, barcode, color, price,
             image, stock, archived, print_to,
             sorting, name, cost) values (-1, 1, '', 0, 1, 0, '', null, 1, null,
             1, 0, '', 0, 0, 0, 0, 'Custom', 0);

             insert into order_order (id, description, close_date, open_date,
             emp_open_id, discount_orders, terminal_id,
             discount_total, subtotal, tax_total, shift_id,
             hold_date, number, customer_id, balance_remaining,
             grand_total, status, emp_close_id) values (-1, null, null, null, null, null, null, 0,
             0, 0, null, null, -1, null, null, 0, 1, null);

             insert into products_store
             (address_2, xweb_terminal_id, zipcode,
             xweb_url, xweb_auth_key, fax,
             xweb_industry, archived, city,
             name, state, number, website,
             email, phone, timezone, tax_rate_id,
             logo, package, xweb_id, address) values ('', '', 10016, '', '', '', '', 0, 'New York',
             'My Store', 'NY', 1, 'biyowallet.com',
             'support@biyowallet.com', '315-325-0050',
             'US/Central', 1, '', 1, '', '1 Biyo Way');

              insert into products_terminal
              (id, mac_id, master, archived, station_number,
              receipt_printer, mode, local_ip, pole_display,
              name) values
              (-1, '*', null, 0, null, null, 2, null,
              'pole1', 'First Terminal');
         """)
    ]
