from django import forms
from employees.models import Employee
from . import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from betterforms.multiform import MultiModelForm
from products.models import Product
from django.db.models import Q
try:
    from collections import OrderedDict
except ImportError:  # Python 2.6, Django < 1.7
    from django.utils.datastructures import SortedDict as OrderedDict  # NOQA


class PinLogin(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('pin',)

    def clean_pin(self):
        pin = self.cleaned_data.get('pin')
        try:
            self.instance = Employee.objects.get(pin=pin)
        except ObjectDoesNotExist:
            raise forms.ValidationError(_('incorrect PIN'))
        return pin


class Purchase(forms.ModelForm):
    class Meta:
        model = models.Purchase
        fields = ('document_number', 'note')


class PurchaseItem(forms.ModelForm):
    product = forms.CharField(label=_('Name or Barcode'), max_length=200)
    entered_stock = forms.IntegerField(label=_('Qty'), min_value=1, initial=1)

    class Meta:
        model = models.PurchaseItem
        fields = ('product', 'entered_stock')

    def clean_product(self):
        product_identity = self.cleaned_data.get('product')
        try:
            return Product.objects.\
                filter(Q(name=product_identity) | Q(barcode=product_identity)).\
                filter(active=True).\
                get()
        except ObjectDoesNotExist:
            raise forms.ValidationError(_('Product not found'))
        except MultipleObjectsReturned:
            raise forms.ValidationError(_('Multiple objects found'))


def purchase_items_form(fields, can_delete=True):
    return forms.modelformset_factory(models.PurchaseItem,
                                      fields=fields,
                                      extra=0,
                                      min_num=0,
                                      can_delete=can_delete)


class FormAction(forms.ModelForm):
    action = forms.ChoiceField(choices=
        (
            ('delete', 'delete'),
            ('ship', 'ship'),
            ('accepted', 'accepted')
        )
    )

    class Meta:
        model = models.Purchase
        fields = ('id',)
