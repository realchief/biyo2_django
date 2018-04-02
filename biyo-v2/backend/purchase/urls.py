# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns

from . import views

urlpatterns = patterns(
    '',
    url(r'^$', views.LoginWithPIN.as_view(), name='login'),
    url(r'^check_product_exist/$', views.CheckProductExist.as_view(), name='check_product_exist'),
    url(r'^orders/$', views.ChoiceOrder.as_view(), name='choice_order'),
    url(r'^order/new/$', views.CreateOrder.as_view(), name='create_order'),
    url(r'^order/(?P<pk>\d+)/draft/$', views.DraftOrder.as_view(), name='order_draft'),
        url(r'^order/(?P<pk>\d+)/draft/info/$', views.DraftOrderPurchase.as_view(), name='order_draft_info'),
        url(r'^order/(?P<pk>\d+)/draft/item/$', views.DraftOrderPurchaseItem.as_view(), name='order_draft_item'),
        url(r'^order/(?P<pk>\d+)/draft/items/$', views.DraftOrderPurchaseItems.as_view(), name='order_draft_items'),
    url(r'^order/(?P<pk>\d+)/shipped/$', views.ShippedOrder.as_view(), name='order_shipped'),
        url(r'^order/(?P<pk>\d+)/shipped/items$', views.ShippedOrderPurchaseItems.as_view(), name='order_shipped_items'),
    url(r'^order/(?P<pk>\d+)/accepted/$', views.AcceptedOrder.as_view(), name='order_accepted'),
    url(r'^order/(?P<pk>\d+)/deleted/$', views.DeletedOrder.as_view(), name='order_deleted'),
)
