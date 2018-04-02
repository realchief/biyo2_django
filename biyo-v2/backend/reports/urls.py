# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns

from . import views

urlpatterns = patterns(
    '',
    
    url(r'^item/sales/$', views.ItemSalesView.as_view(), name='item_sales'),
    url(r'^item/sales/pdf/$', views.ItemSalesPDFView.as_view(), name='item_sales_pdf'),
    url(r'^sales_summary/$', views.SalesSummaryView.as_view(), name='sales_summary'),
    url(r'^sales_summary/pdf/$', views.SalesSummaryPDFView.as_view(), name='sales_summary_pdf'),
    url(r'^employee_sales_summary/$', views.EmployeeSalesSummaryView.as_view(), name='employee_sales_summary'),
    url(r'^discount_summary/$', views.DiscountSummary.as_view(), name='discount_summary'),
    url(r'^hourly_sales/$', views.HourlySales.as_view(), name='hourly_sales'),
    url(r'^order_gross_profit/$', views.OrderGrossProfit.as_view(), name='order_gross_profit'),
    # url(r'^accountant_summary/$', views.AccountantSummary.as_view(), name='accountant_summary'),

    url(r'^category_summary/$', views.AccountantSummary.as_view(), name='accountant_summary'),
    url(r'^accountant_summary/test$', views.TestReport.as_view(), name='accountant_test'),
    url(r'^customer-payment/(?P<pk>\d+)/$', views.CustomerPaymentView.as_view(), name='customer-payment'),
    url(r'^ajax-customer-orders/(?P<pk>\d+)/$', views.CustomerOrderAjaxView.as_view(), name='ajax-customer-orders'),

    # New
    url(r'^item/price_adjustments/$', views.PriceAdjustments.as_view(), name='price_adjustment'),
    url(r'^product/(?P<pk>\-?\d+)/vieworders/$', views.ProductViewOrders.as_view(), name='product_view_orders'),


    url(r'^employee_hour_summary/$', views.EmployeeTotalHourSummaryReport.as_view(), name='employee_hour_summary'),
    url(r'^time_card_weekly/$', views.TimeCardWeeklyReport.as_view(), name='time_card_weekly'),
    url(r'^time_card_weekly/pdf$', views.TimeCardWeeklyPDFReport.as_view(), name='time_card_weekly_pdf'),
    url(r'^employee_hour_edit/(?P<pk>\d+)$$', views.EditEmployeeTotalHourSummaryReport.as_view(),
        name='edit_employee_hour_summary'),
    url(r'^order_types/$', views.OrderTypesReport.as_view(), name='order_types'),
    url(r'^payments/$', views.PaymentView.as_view(), name='reports_payments'),
    url(r'^top_customers/$', views.TopCustomersView.as_view(), name='top_customers'),
    url(r'^dashboardcharts/$', views.GetSalesAndOrdersDashboard.as_view(), name='dashboardcahrts'),
    url(r'^orders/discounted/$', views.DiscountedOrdersView.as_view(), name='discounted_orders'),

    url(r'^payouts/$', views.PayoutsView.as_view(), name='payouts_orders'),




    url(r'^check-orders2/$', views.CheckOrdersAndPayments.as_view(), name='check_orders_payments'),
    url(r'^check-orders/$', views.CheckOrders.as_view(), name='check_orders'),
    url(r'^check-item-match/$', views.CheckOrdderMatch.as_view(), name='check_orders_item'),
    url(r'^customers-report/$', views.CustomerReport.as_view(), name='customer-report-view'),


    url(r'^$', views.CustomerReport.as_view(), name='reports_home'),

)
