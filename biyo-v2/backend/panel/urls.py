# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns, include

from order.views import SharedOrderView
from . import views
from taskin import views as taskin_views
from panel.views import change_password


urlpatterns = patterns(
    '',
    url(
        r'^dashboard/$',
        views.DashboardView.as_view(),
        name='dashboard'
    ),
    url(r'^', include(views.printer_crud.urls)),

    url(r'^', include(views.time_crud.urls)),
    url(r'^', include(views.rewards_crud.urls)),



    url(r'^', include(views.product_crud.urls)),
    url(r'^', include(views.modifier_group_crud.urls)),
    url(r'^', include(views.modifier_crud.urls)),
    url(r'^', include(views.category_crud.urls)),
    url(r'^', include(views.tax_rate_crud.urls)),
    url(r'^', include(views.discount_crud.urls)),
    url(r'^', include(views.employee_crud.urls)),
    url(r'^', include(views.order_crud.urls)),
    url(r'^', include(views.customer_crud.urls)),
    url(r'^', include(views.supplier_crud.urls)),
    url(r'^', include(views.table_crud.urls)),
    url(r'^', include(views.tablesection_crud.urls)),
    url(r'^', include(views.store_crud.urls)),
    url(r'^', include(views.terminal_crud.urls)),
    url(r'^', include(views.taskin_group_crud.urls)),

    # taskin views
    url(r'^', include(taskin_views.taskinspicialprices_group_crud.urls)),


    url(r'^ordersortlistclean/$', views.OrderSortListClean, name='ordersortlistclean'),
    url(r'^orders/$', views.OrderListView.as_view(), name='order-list'),
    url(r'^order/add/items$', views.OrderItemListView.as_view(), name='order-add-items', ),
    url(r'^order/(?P<pk>-?\d+)/edit/items/', views.OrderItemListView.as_view(), name='order-update', ),
    url(r'^order/add/payment$', views.OrderPaymentView.as_view(), name='order-add-payment', ),
    url(r'^orders/(?P<pk>-?\d+)/$', views.OrderDetailView.as_view(), name='order-detail'),
    url(r'^orders/(?P<pk>-?\d+)/update/$', views.OrderUpdateView.as_view()),
    url(r'^orders/shared/(?P<slug>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$',
        SharedOrderView.as_view()),
    url(r'^employeechangepass/(?P<pk>\d+)/$', change_password, name='empl_changepass'),
    url(r'^quickproductadd/$', views.QuickProductAdd.as_view(), name='quick_product_add'),
    url(r'^products/import/$', views.CsvParserView.as_view(), name='import_csv'),
    url(r'^csv-parse-customer/$', views.CsvParserCustomer.as_view(), name='csvparsecustomer'),
    url(r'^csvdownload/$', views.ProductExportCsvView.as_view(), name='csvdownload'),
    url(r'^csvcustomerdownload/$', views.CustomerExportCsvView.as_view(), name='csvcustomerdownload'),
    url(r'^clearfilterproduct', views.ClearFilterProduct.as_view(), name='clearfilterproduct')
)
