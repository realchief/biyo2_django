from django.views.generic import FormView, UpdateView, ListView, DetailView, View
from . import forms
from . import models
from employees.models import Employee
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.utils.decorators import method_decorator
from decorators import pin_auth_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import resolve
from django.db.models import Q
from django.utils import timezone
from django.http import JsonResponse
from products.models import Product
from purchase.models import PurchaseItem
from panel.crud import DeleteView


class LoginWithPIN(FormView):
    template_name = 'purchase/quick/login.html'
    form_class = forms.PinLogin
    success_url = reverse_lazy('quick:choice_order')

    def get(self, request, *args, **kwargs):
        if 'employee_id' in request.session:
            return HttpResponseRedirect(self.success_url)
        return super(LoginWithPIN, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        self.request.session['employee_id'] = form.instance.id
        return super(LoginWithPIN, self).form_valid(form)


class BaseAuth(object):
    @method_decorator(pin_auth_required)
    def dispatch(self, request, *args, **kwargs):
        '''
        Auth required
        '''
        return super(BaseAuth, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kw):
        '''
        The base template depending of user authentication type.
        '''
        context = super(BaseAuth, self).get_context_data(**kw)
        if 'employee_id' in self.request.session:
            context['base_template'] = 'purchase/quick/base.html'
        else:
            context['base_template'] = 'base.html'
        return context


class BaseQueryset(object):
    def get_queryset(self):
        '''
        Get all available purchase of current employee
        '''
        if 'employee_id' in self.request.session:
            self.employee = get_object_or_404(Employee, pk=self.request.session['employee_id'])
        else:
            self.employee = self.request.user
        return models.Purchase.objects.filter(
                    Q(employee_created=self.employee) | Q(employee_update=self.employee)
                )


class ChoiceOrder(BaseAuth, BaseQueryset, ListView):
    '''
    Choice order from available list or create new
    '''
    template_name = 'purchase/quick/list.html'


class CreateOrder(BaseAuth, BaseQueryset, View):
    def get(self, request, *args, **kwargs):
        self.get_queryset()
        instance = models.Purchase.objects.create(
            employee_created=self.employee,
        )
        return HttpResponseRedirect(instance.get_absolute_url())


##### Draft
class DraftOrder(BaseAuth, BaseQueryset, UpdateView):
    '''
    Draft stage of purchase order wizzard. Contains 4 forms
    1) FormAction -> Delete, Shipped
    2) Purchase -> Document number, notice
    3) Purchase item -> Add prodcut to list
    4) Purchase item list -> List of added products
    '''

    template_name = 'purchase/quick/draft.html'
    form_class = forms.FormAction

    def get_context_data(self, **kw):
        context = super(DraftOrder, self).get_context_data(**kw)
        context['purchase'] = DraftOrderPurchase.form_class(instance=self.object)
        context['purchase_item'] = DraftOrderPurchaseItem.form_class()
        context['purchase_items'] = DraftOrderPurchaseItems\
            .form_class(queryset=self.object.purchase_items.all())
        return context

    def form_valid(self, form):
        action = form.cleaned_data.get('action')
        instance = form.save(commit=False)
        if action == 'delete':
            instance.status = 'deleted'
        else:
            instance.status = 'shipped'
            instance.shipped_dt = timezone.now()
        instance.save()
        return HttpResponseRedirect(self.object.get_absolute_url())


class DraftOrderPurchase(BaseAuth, BaseQueryset, UpdateView):
    '''
    Purchase form -> Document number, notice
    '''
    form_class = forms.Purchase

    def form_invalid(self, form):
        return JsonResponse(form.errors)


class DraftOrderPurchaseItem(BaseAuth, BaseQueryset, UpdateView):
    '''
    Purchase item -> Add product to selected Purchase
    '''
    form_class = forms.PurchaseItem

    def get_form_kwargs(self):
        kwargs = super(UpdateView, self).get_form_kwargs()
        kwargs.update(instance=self.form_class._meta.model())
        return kwargs

    def form_valid(self, form):
        item = form.save(commit=False)
        item.purchase = self.object
        item.accepted_stock = item.entered_stock
        item.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return JsonResponse(form.errors)


class DraftOrderPurchaseItems(BaseAuth, BaseQueryset, UpdateView):
    '''
    List of available items for current purchases
    '''
    form_class = forms.purchase_items_form(fields=('entered_stock', ))

    def get_form_kwargs(self):
        kwargs = super(UpdateView, self).get_form_kwargs()
        instance = kwargs.pop('instance')
        kwargs.update(queryset=instance.purchase_items.all())
        return kwargs

    def form_valid(self, form):
        items = form.save()
        for item in items:
            item.accepted_stock = item.entered_stock
            item.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return JsonResponse(form.errors)


##### Shipped
class ShippedOrder(BaseAuth, BaseQueryset, UpdateView):
    '''
    Shipped stage of purchase order wizzard.
    '''
    template_name = 'purchase/quick/shipped.html'
    form_class = forms.FormAction

    def get_context_data(self, **kw):
        context = super(ShippedOrder, self).get_context_data(**kw)
        context['purchase_items'] = ShippedOrderPurchaseItems\
            .form_class(queryset=self.object.purchase_items.all())
        return context

    def form_valid(self, form):
        action = form.cleaned_data.get('action')
        instance = form.save(commit=False)
        instance.status = action
        if action == 'accepted':
            purchases = PurchaseItem.objects.filter(purchase=instance)
            for purchase in purchases:
                product_total = purchase.total
                product_id = purchase.product_id
                Product.objects.filter(id=product_id).update(stock=product_total)
        instance.accepted_dt = timezone.now()
        instance.save()
        return HttpResponseRedirect(self.object.get_absolute_url())


class ShippedOrderPurchaseItems(BaseAuth, BaseQueryset, UpdateView):
    form_class = forms.purchase_items_form(fields=('accepted_stock', ),
                                           can_delete=False)

    def get_form_kwargs(self):
        kwargs = super(UpdateView, self).get_form_kwargs()
        instance = kwargs.pop('instance')
        kwargs.update(queryset=instance.purchase_items.all())
        return kwargs

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return JsonResponse(form.errors)

##### Accepted
class AcceptedOrder(BaseAuth, BaseQueryset, DetailView):
    template_name = 'purchase/quick/accepted.html'
    model = models.Purchase


##### Deleted
class DeletedOrder(BaseAuth, BaseQueryset, UpdateView):
    template_name = 'purchase/quick/deleted.html'


class CheckProductExist(BaseAuth, BaseQueryset, View):
    '''
    Purchase form -> Document number, notice
    '''
    def post(self, request, *a, **kw):
        from django.db.models import Q
        product_name = request.POST.get('product')
        try:
            product = Product.objects.get(Q(barcode=product_name)|Q(name=product_name))
            return JsonResponse({'product': product.id})
        except ObjectDoesNotExist:
            return JsonResponse({'product': None})
