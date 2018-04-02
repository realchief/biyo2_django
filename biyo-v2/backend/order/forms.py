"""
This module is responsible for keeping and accessing to base forms related to Order model and it's siblings.
"""

__author__ = 'Konstantin Oficerov'
__email__ = 'konstantin.oficerov@crystalnix.com'

from django import forms
from .models import *
from employees.models import Employee, Customer
from payments.models import Shift, Payment
from products.models import Terminal, Discount


class OrderItemForm(forms.ModelForm):
    """
    Form is supposed to serialize OrderItem model and provide create-read-update functionality.
    Customized constructor takes advanced order_id field which is actually PK of 'order' field.
    """
    order_id = forms.IntegerField(widget=forms.HiddenInput())
    instance_id = forms.IntegerField(widget=forms.HiddenInput())
    # terminal_id = forms.ModelChoiceField(Terminal.objects.all(), required=True, label="Terminal", )

    def __init__(self, **kwargs):
        instance = kwargs.get('instance', None)
        if instance:
            kwargs['initial'] = kwargs.get('initial', {})
            kwargs['initial']['order_id'] = instance.order.id
            kwargs['initial']['instance_id'] = instance.id
        super(OrderItemForm, self).__init__(**kwargs)

    class Meta:
        model = OrderItem
        fields = (
            "name",
            "price",
            "cost",
            "discount",
            "tax",
            "employee",
            "product",
            "quantity",
            "void_status",
        )

        widgets = {
            'void_status': forms.HiddenInput(),
            'cost': forms.HiddenInput(),
            'price': forms.HiddenInput(),
            'employee': forms.HiddenInput(),
            'product': forms.HiddenInput(),
            'name': forms.TextInput(attrs={"autocomplete": "off", "class": "span3", }),
            'tax': forms.NumberInput(attrs={"class": "span2", }),
            'discount': forms.NumberInput(attrs={"class": "span1", }),
            'quantity': forms.NumberInput(attrs={"class": "span1", }),
        }


class OrderForm(forms.ModelForm):
    """
    Form is supposed to serialize model Order and provide create-read-update functionality.
    """

    emp_open_id = forms.ModelChoiceField(Employee.objects.all(), required=True, label="Employee open",
                                         widget=forms.HiddenInput())
    emp_close_id = forms.ModelChoiceField(Employee.objects.all(), required=False, label="Employee close",
                                          widget=forms.HiddenInput())
    customer_id = forms.ModelChoiceField(Customer.objects.all(), required=False, label="Customer",
                                         widget=forms.Select(attrs={'class': 'span12', }))
    # shift_id = forms.ModelChoiceField(Shift.objects.all(), required=False, label="Shift",
    #                                   widget=forms.Select(attrs={'class': 'span12', }))
    # terminal_id = forms.ModelChoiceField(Terminal.objects.all(), required=True, label="Terminal",
    #                                      widget=forms.HiddenInput())

    class Meta:
        model = Order
        fields = (
            "number",
            "subtotal",
            "tax_total",
            "discount_total",
            "grand_total",
            "open_date",
            "hold_date",
            "close_date",
            "status",
            "description",
            "discount_orders",
            "balance_remaining",
        )
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Invoice Notes', 'class': 'span12', 'rows': '4', }),
            # 'terminal_id': forms.NumberInput(attrs={'class': 'span3', 'required': True}),
            'number': forms.HiddenInput(),
            "balance_remaining": forms.HiddenInput(),
            "status": forms.HiddenInput(attrs={'required': True}),
            "subtotal": forms.HiddenInput(attrs={'required': True}),
            "tax_total": forms.HiddenInput(attrs={'required': True}),
            "discount_total": forms.HiddenInput(attrs={'required': True}),
            "grand_total": forms.HiddenInput(attrs={'required': True}),
            "discount_orders": forms.NumberInput(attrs={'label': "Order's discount",
                                                        'placeholder': "Discount for whole order",
                                                        'class': 'span11',
                                                        }),
            "open_date": forms.HiddenInput(),
            "hold_date": forms.HiddenInput(),
            "close_date": forms.HiddenInput(),
        }


class OrderModifierForm(forms.ModelForm):
    """
    Form is supposed to serialize OrderModifier model and provide read functionality.
    """
    item_id = forms.IntegerField(widget=forms.HiddenInput())
    oryginal_id = forms.IntegerField(required=True, widget=forms.HiddenInput())
    group_id = forms.IntegerField(required=True, widget=forms.HiddenInput())
    instance_id = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, **kwargs):
        instance = kwargs.get('instance', None)
        if instance:
            kwargs['initial'] = kwargs.get('initial', {})
            kwargs['initial']['item_id'] = instance.item.id
            kwargs['initial']['instance_id'] = instance.id
            kwargs['initial']['group_id'] = instance.group.id
            kwargs['initial']['oryginal_id'] = instance.oryginal.id
        super(OrderModifierForm, self).__init__(**kwargs)

    class Meta:
        model = OrderModifier
        fields = (
            'name',
            'cost',
            'price',
            'void_status',
        )

        widgets = {
            'void_status': forms.HiddenInput(),
            'name': forms.TextInput(attrs={'required': True, 'class': "span8", "placeholder": 'Put the name here', }),
            'cost': forms.HiddenInput(attrs={'required': True, 'class': "span12", "placeholder": 'Cost', }),
            'price': forms.HiddenInput(attrs={'required': True, 'class': "span12", "placeholder": 'Price', }),
        }


class OrderPaymentForm(forms.ModelForm):
    """
    Form is supposed to serialize Payment model to organize further request within "terminalapi".
    """
    employee_id = forms.IntegerField(required=True, widget=forms.HiddenInput(), )
    order_id = forms.IntegerField(required=True, widget=forms.HiddenInput(), )

    class Meta:
        model = Payment
        fields = (
            "amount",
            "amount_paid",
            "tips",
            "change_amount",
            "card_lastfour",
            "payment_type",
            "payment_date",
            "payment_form",
            "authorization",
            "transaction_type",
            "processor_response",
            "batch_num",
            "approval_code",
            "transaction_id",
            "terminal_id",
            "signature",
            "void_ref",
            'check_number',
        )

        widgets = dict()
        for field in fields:
            widgets[field] = forms.HiddenInput()
        widgets["amount"] = forms.NumberInput(attrs={
            "class": "span12",
            "min": "0",
            "style": "text-align:right;margin-bottom:4px;background:#7986CB;color:white;"
        })


class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ()
