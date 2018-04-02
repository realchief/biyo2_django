import pytz
from django.shortcuts import redirect
from django.views.generic import DetailView
from products import models as products_models
from order.models import SharedOrder
from products.models import Store


class SharedOrderView(DetailView):
    model = SharedOrder
    template_name = 'shared_order.html'

    def get_slug_field(self):
        return 'identifier'

    def get_queryset(self):
        if not self.request.user:
            return redirect('/')
        return super(SharedOrderView, self).get_queryset()

    def get_context_data(self, **kwargs):
        order_items = self.object.order.items.all().exclude(void_status=1)
        voided_order_items = self.object.order.items.filter(void_status=1)
        customer = self.object.order.customer
        store = Store.objects.first()
        tz = products_models.Store.objects.first().timezone
        tz = pytz.timezone(tz)
        return {
            'object': self.object,
            'order_items': order_items,
            'voided_items': voided_order_items,
            'customer': customer,
            'tz': tz,
            'store': store
        }
