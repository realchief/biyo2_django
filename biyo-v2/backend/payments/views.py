from django.http.response import HttpResponseRedirect
from django.views.generic.edit import UpdateView
from panel import decorators
from django.contrib.auth.decorators import login_required
from panel.views import ModelFormWithMessageMixin
from payments.forms import AddTipsForm
from payments.models import Payment
from products.models import Store
import urllib
from django.core.urlresolvers import reverse

@decorators.dispatch_decorator(login_required)
class AddTips(ModelFormWithMessageMixin, UpdateView):
    model = Payment
    template_name = 'addtips.html'


    def post(self, request, *args, **kwargs):
        object = self.get_object()
        form = AddTipsForm(self.request.POST)
        if form.is_valid():
            store = Store.objects.get(pk=1)
            data = {
                'XWebID': store.xweb_id,
                'TerminalID': store.xweb_terminal_id,
                'AuthKey':store.xweb_auth_key,
                'SpecVersion':'XWeb3.4',
                'Industry':store.xweb_industry,
                'POSType':'PC',
                'PinCapabilities':'FALSE',
                'TrackCapabilities':'NONE',
                'TransactionType':'CreditUpdateTransaction',
                'TransactionID':object.transaction_id,
                'GratuityAmount':self.request.POST.get('value')
                }
            body = urllib.urlencode(data)
            import requests
            str =store.xweb_url+'?'+body
            requests.get(str, verify=False)
            return HttpResponseRedirect(reverse('order-detail',kwargs={'pk':object.order.id}))
        return super(AddTips,self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        form = AddTipsForm(self.request.POST)
        return {'form':form}