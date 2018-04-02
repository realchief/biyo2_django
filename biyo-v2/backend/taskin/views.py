import json
from django.http.response import HttpResponse
from panel.views import LoginReqListView, ExtendModelCrud, MessageUpdateView
from products.models import Product
from taskin.forms import TaskinSpecialPricesForm
from taskin.models import SpecialPrices, CustomerGroup


class TaskinSpecialPricesGroupCreateView(LoginReqListView):
    # form_model = CustomerForm
    pass


class UpdateTaskinSpecialPricesView(MessageUpdateView):
    form_class = TaskinSpecialPricesForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.is_ajax():

            name = request.POST.get('name', False)
            if name == 'group':
                self.object.group = CustomerGroup.objects.get(pk=request.POST.get('value'))
            elif name == 'product':
                self.object.product = Product.objects.get(pk=request.POST.get('value'))
            else:
                setattr(self.object, request.POST.get('name'), request.POST.get('value'))
            self.object.save()
            # return shortcuts.redirect(self.get_success_url())
            return HttpResponse(json.dumps({'status': '200'}), content_type="application/json")
        else:
            return super(UpdateTaskinSpecialPricesView, self).post(request, *args, **kwargs)


class TaskinSpecialPrices_Crud(ExtendModelCrud):
    update_class_view = UpdateTaskinSpecialPricesView

taskinspicialprices_group_crud = TaskinSpecialPrices_Crud(
    model=SpecialPrices
)
