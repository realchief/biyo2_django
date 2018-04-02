from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from terminalapi.views import ClearSales
from dbsettings.api import get_settings_by_terminal_pk, get_all_dbsettings

urlpatterns = patterns(
    'terminalapi.views',
    url(r'^sync/employees$', 'sync_employees'),
    url(r'^sync/customers$', 'sync_customers'),
    url(r'^sync/suppliers$', 'sync_suppliers'),
    url(r'^sync/payments$', 'sync_payments'),
    url(r'^sync/orders$', 'sync_orders'),
    url(r'^sync/orders/items$', 'sync_orders_items'),
    url(r'^sync/orders/modifiers$', 'sync_orders_modifiers'),
    url(r'^sync/orders/options$', 'sync_orders_options'),
    url(r'^sync/products$', 'sync_products'),
    url(r'^sync/products/id/name$', 'get_product_id_name'),
    url(r'^sync/products/advanced$', 'sync_products_advanced'),
    url(r'^sync/products/special-prices$', 'show_special_prices'),
    url(r'^sync/modifiers_groups$', 'sync_modifiers_groups'),
    url(r'^sync/modifiers$', 'sync_modifiers'),
    url(r'^sync/taxrates$', 'sync_taxrate'),
    url(r'^sync/categories$', 'sync_categories'),
    url(r'^sync/discount$', 'sync_discount'),
    url(r'^sync/store$', 'sync_store'),
    url(r'^sync/table$', 'sync_table'),
    url(r'^sync/tablesection$', 'sync_tablesection'),
    url(r'^sync/terminal$', 'sync_terminal'),
    url(r'^sync/prod2cat$', 'sync_prod2cat'),
    url(r'^sync/prod2mg$', 'sync_prod2mg'),
    url(r'^sync/taskingroups$', 'sync_taskingroups'),

    url(r'^sync/sales_payments$', 'sales_payments'),

    url(r'^sync/printer$', 'sync_printer'),
    url(r'^sync/timeclock$', 'timeclock'),
    url(r'^sync/rewardcampaigns$', 'rewardcampaigns'),

    url(r'^sync/shifts$', 'sync_shifts'),
    url(r'^sync/payouts$', 'sync_payouts'),

    url(r'^add/order$', 'add_order'),
    url(r'^add/order/item$', 'add_order_item'),
    url(r'^add/order/item/modifier$', 'add_order_item_modifier'),
    url(r'^add/payments$', 'add_payment'),
    url(r'^add/customer', 'add_customer'),
    url(r'^add/employee', 'add_employee'),
    url(r'^add/tax', 'add_tax'),
    url(r'^add/store', 'add_store'),
    url(r'^add/product', 'add_product'),

    url(r'^add/printer', 'add_printer'),

    url(r'^add/shift', 'add_shift'),
    url(r'^add/payout', 'add_payout'),

    url(r'^update/order/(?P<pk>\d+)$', 'update_order'),
    url(r'^update/order/item/(?P<pk>\d+)$', 'update_order_item'),
    url(r'^update/order/item/modifier/(?P<pk>\d+)$', 'update_order_item_modifier'),
    url(r'^update/payments/(?P<pk>\d+)$', 'update_payment'),
    url(r'^update/customer/(?P<pk>\d+)$', 'update_customer'),
    url(r'^update/employee/(?P<pk>\d+)$', 'update_employee'),
    url(r'^update/table/(?P<pk>\d+)$', 'update_table'),
    url(r'^update/box_coords/(?P<pk>\d+)$', 'update_box_coords'),
    url(r'^update/printer/(?P<pk>\d+)$', 'update_printer'),

    url(r'^update/spicialprices/(?P<pk>\d+)$', 'update_spicialprices'),

    url(r'^update/shift/(?P<pk>\d+)$', 'update_shift'),
    url(r'^update/payout/(?P<pk>\d+)$', 'update_payout'),

    url(r'^clear_sales$', ClearSales.as_view()),

    url(r'^get/shift/(?P<pk>\d+)$', 'get_shift'),
    url(r'^get/payout/(?P<pk>\d+)$', 'get_payout'),

    url(r'^check/terminal/mac_id$', 'check_terminal_mac_id'),
    url(r'^check/product/barcode$', 'check_product_barcode'),
    url(r'^check/product/barcode_extended$', 'check_product_barcode_extended'),
    url(r'^check/owner$', 'check_owner'),
    url(r'^get/detailed_orders$', 'get_detailed_orders'),
    url(r'^get/detailed_order/(?P<pk>\d+)$', 'get_detailed_order'),
    url(r'^get/detailed_tables$', 'get_detailed_tables'),

    url(r'^get/customer_balance/(?P<pk>\d+)$', 'get_customer_balance'),

    url(r'^add/timeclock_entry$', 'add_timeclock_entry'),

    url(r'^check/version$', 'check_version'),

    url(r'^get/timeclock_id/(?P<pk>\d+)$', 'get_timeclock_id'),

    url(r'^set/display_box/element/(?P<pk>\d+)$', 'set_display_box_element'),
    url(r'^get/display_box/element/(?P<pk>\d+)$', 'get_display_box_element'),

    url(r'^display_box/removeelement/(?P<pk>\d+)$', 'remove_display_box_element'),

    url(r'^get/employee/(?P<pk>\d+)$', 'get_employee'),

    url(r'^product/get/list$', 'get_cat_list', name='get_prodcat_list'),
    url(r'^modifier/get/list$', 'get_modifier_group_list', name='get_modifier_group_list'),

    url(r'^product/update/list$', 'updateProductCategory', name='update_prod_list'),
    url(r'^modifiers/update/list$', 'updateModifiers', name='update_mods_list'),

    url(r'^get_category_by_id$', 'get_cats'),

    url(r'^run/tests$', 'run_tests'),

    url(r'^settings/get_for_terminal_(?P<pk>\d+)$', get_settings_by_terminal_pk, name='get_settings_by_terminal_pk'),
    url(r'^sync/dbsettings/$', get_all_dbsettings, name='get_all_dbsettings'),
    url(r'^settings/get$', get_settings_by_terminal_pk, name='get_settings_without_terminal_pk')

)

urlpatterns = format_suffix_patterns(urlpatterns)
