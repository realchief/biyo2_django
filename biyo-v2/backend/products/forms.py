from types import NoneType
from django import forms
from django.core.exceptions import ValidationError
from products.models import (Product, COLORS, Category, ModifierGroup, Modifier, TableSection, TaxRate,
                             Printer, Reward, Csv, Terminal, Store)
from django.utils.safestring import mark_safe
from employees.models import TimeClock, Employee, Customer
from django.contrib.admin import widgets
from django.utils import html
import pytz
from django.forms.util import from_current_timezone
from django.forms.util import to_current_timezone
from django.utils import timezone
import datetime


class TableSectionForm(forms.ModelForm):
    class Meta:
        model = TableSection
        fields = ('section_name', 'store')


class PrinterForm(forms.ModelForm):
    class Meta:
        model = Printer
        fields = ('name', 'local_ip')


class RewardsForm(forms.ModelForm):

    class Meta:
        model = Reward
        fields = ('name', 'store', 'points_redeem', 'discount', 'discount_type', 'reward_type',
                  'discount_type_item', 'discount_value', 'discount_text',)
        widgets = {
            'discount_value': forms.NumberInput(attrs={'max': 99999999})
        }

    # def __init__(self, *args, **kw):
    #     super(RewardsForm, self).__init__(*args, **kw)
    #     self.fields.keyOrder = [
    #        'name','store','points_reedem','discount','discount_type','reward_type','discount_type_item','discount_value','discount_text',]

    def clean_discount_value(self):
        form_data = super(RewardsForm, self).clean()

        try:
            value = int(form_data['discount_value'])
        except Exception as e:
            raise forms.ValidationError(u'Must be number')
        if (form_data['discount_type'] == 'Item'):
            if (form_data['reward_type'] == 1):
                if value > 100:
                    raise forms.ValidationError(u'%s cannot be more than 100' % value)
                if value < 0:
                    raise forms.ValidationError(u'%s cannot be less than 0' % value)
            if (form_data['reward_type'] == 2):
                item = form_data['discount_type_item']
                if (value) > item.price:
                    raise forms.ValidationError(
                        u'Item price: $%s. Discount $%d cannot be more than price.' % (item.price, value))
        return value


class TimeClockFastAdd(forms.ModelForm):
    time_in = forms.DateTimeField(required=False)
    time_out = forms.DateTimeField(required=False)
    # employee = forms.ModelChoiceField(queryset=Employee.objects.all().exclude(archived=True))

    class Meta:
        model = TimeClock
        fields = ('time_in', 'time_out')


class TzAwareTimeField(forms.fields.DateTimeField):

    def prepare_value(self, value):
        if isinstance(value, datetime.datetime):
            value = to_current_timezone(value)
        return super(TzAwareTimeField, self).prepare_value(value)

    def clean(self, value):
        from pytz import timezone
        value = super(TzAwareTimeField, self).to_python(value)
        tz = Store.objects.get(pk=1).timezone
        dt = value.astimezone(timezone(tz))
        return dt.replace(
            day=value.day, month=value.month, year=value.year,
            hour=value.hour, minute=value.minute,
            second=value.second, microsecond=value.microsecond)


class TimeClockForm(forms.ModelForm):

    time_in = TzAwareTimeField(
        required=True, widget=forms.DateTimeInput(format='%Y-%m-%d %I:%M %p'), input_formats=('%Y-%m-%d %I:%M %p',))
    time_out = TzAwareTimeField(
        required=False, widget=forms.DateTimeInput(format='%Y-%m-%d %I:%M %p'), input_formats=('%Y-%m-%d %I:%M %p',))
    employee = forms.ModelChoiceField(queryset=Employee.objects.all().exclude(archived=True))

    class Meta:
        model = TimeClock
        fields = ('employee', 'time_in', 'time_out')


class FileImageWidget(forms.FileInput):
    """
    A ImageField Widget that shows a thumbnail.
    """

    def __init__(self, attrs={}):
        super(FileImageWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output = []
        if value and hasattr(value, "url"):
            output.append(('<a target="_blank" href="%s">'
                           '<img src="%s" style="height: 150px;" /></a>'
                           % (value.url, value.url)))
        output.append(super(FileImageWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))


class ProductCategoryForm(forms.Form):
    categories = forms.ChoiceField(label="", help_text="", widget=forms.Select,
                                   required=False)

    def __init__(self, *args, **kwargs):
        super(ProductCategoryForm, self).__init__(*args, **kwargs)
        cats = Category.objects.exclude(archived=True).all()
        choices = []
        choices.append(('', 'All Categories'))
        choices.append(('None', '--Uncategorized--'))
        for cat in cats:
            choices.append((cat.id, cat.name))
        self.fields["categories"].choices = choices


class ProductMultipleCategoryForm(forms.Form):
    multiple_categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.exclude(archived=True)
    )

    def __init__(self):
        super(ProductMultipleCategoryForm, self).__init__()


PAYMENTS = (
    ('', 'All Payment Types'),
    ('Cash', 'Cash'),
    ('Account', 'Account'),
    ('Visa', 'Visa'),
    ('MasterCard', 'MasterCard'),
    ('OtherCredit', 'OtherCredit'),
    ('American Express', 'American Express'),
    ('allcards', 'All Cards')
)

STATUS = (
    ('', ' All Statuses'),
    ('1', 'Open'),
    ('2', 'Hold'),
    ('3', 'Closed'),
    ('4', 'Canceled'),
    ('5', 'Refunded'),
)


class OrderSortForm(forms.Form):
    # date_range = forms.CharField(max_length=100, initial='Today', help_text="")
    status = forms.ChoiceField(label="", help_text="", widget=forms.Select,
                               choices=STATUS, required=False)

    employees = forms.ModelChoiceField(label="", help_text="", widget=forms.Select, empty_label='All Employees',
                                       queryset=Employee.objects.all().exclude(archived=True), required=False)
    terminal = forms.ModelChoiceField(label="", help_text="", widget=forms.Select, empty_label='All Terminals',
                                      queryset=Terminal.objects.all().exclude(archived=True), required=False)

    payment = forms.ChoiceField(label="", help_text="", widget=forms.Select,
                                choices=PAYMENTS, required=False)
    customer = forms.ModelChoiceField(label="", help_text="", widget=forms.Select,
                                      queryset=Customer.objects.exclude(archived=1), empty_label='All Customers',
                                      required=False)

    def __init__(self, request, *args, **kwargs):
        super(OrderSortForm, self).__init__(*args, **kwargs)

        self.fields["employees"].initial = request.session.get('employee')
        self.fields["status"].initial = request.session.get('status')
        self.fields["payment"].initial = request.session.get('payment')
        self.fields["terminal"].initial = request.session.get('terminal')
        self.fields["customer"].initial = request.session.get('customer')


class SubmitButtonWidget(forms.Widget):
    def render(self, name, value, attrs=None):
        return '<input type="submit" name="%s" value="%s">' % (html.escape(name), html.escape("Remove Image"))


class BaseProductCategory(forms.ModelForm):
    remove_photo = forms.BooleanField(required=False, label='', widget=SubmitButtonWidget(attrs={'class': 'ck-button'}))

    def __init__(self, *args, **kwargs):
        super(BaseProductCategory, self).__init__(*args, **kwargs)
        if bool(self.instance.image) is False:
            del self.fields["remove_photo"]

    def save(self, commit=True):
        self.instance.change_reason = "Update product"
        self.instance.stock_change = 0
        instance = super(BaseProductCategory, self).save(commit=True)
        if self.cleaned_data.get('remove_photo'):
            try:
                import os
                os.unlink(instance.image.path)

            except OSError:
                pass
            instance.image = None
            if commit:
                instance.save()
        return instance


class ProductForm(BaseProductCategory):
    color = forms.ChoiceField(choices=COLORS, widget=forms.RadioSelect(attrs={'style': 'hidden'}))
    modifier_groups = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(attrs={
        'class': 'selectpicker product-creation-select form-control',
        'multiple': '',
        'data-style': 'btn-secondary',
        'data-size': '5',
    }),
        queryset=ModifierGroup.objects.all().exclude(archived=True),
                                                     required=False)
    categories = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(attrs={
        'class': 'selectpicker product-creation-select form-control',
        'multiple': '',
        'data-style': 'btn-secondary',
        'data-size': '5',
        'required': 'True'
    }),
                                                queryset=Category.objects.all().exclude(archived=True),
                                                required=True)
    tax_rate = forms.ModelChoiceField(queryset=TaxRate.objects.all().exclude(archived=True), empty_label="No Selected")

    printer = forms.ModelChoiceField(queryset=Printer.objects.all().exclude(archived=True), empty_label="No Selected")

    image = forms.ImageField(widget=FileImageWidget, required=False)

    price_adjust = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        # XXX: TaxRate table maybe clean.
        self.fields["tax_rate"].initial = TaxRate.objects.get(id=1)
        self.fields["price_adjust"].initial = False
        if 'instance' in kwargs:
            try:
                self.id = kwargs['instance'].id
            except AttributeError:
                pass

    def clean_barcode(self):
        barcode = self.cleaned_data['barcode']
        if barcode == "" or barcode == "0.0":
            return barcode
        qs = Product.objects.filter(barcode=barcode).exclude(archived=True)
        try:
            if self.id:
                qs = qs.exclude(pk=self.id)
        except AttributeError:
            pass
        if qs.count() > 0:
                raise ValidationError('This barcode is already in use.')
        return barcode

    def clean_active(self, *args, **kwargs):
        return self.initial.get('active', True)

    def save(self, *args, **kwargs):
        if self.instance.id:
            self.instance.change_reason = "Update product"
        else:
            self.instance.change_reason = "Create product"
        self.instance.stock_change = 0

        if not self.files:
            self.instance.image = None
        return super(ProductForm, self).save(*args, **kwargs)

    class Meta:
        model = Product
        fields = ('name', 'description', 'image', 'remove_photo', 'color', 'categories', 'sorting',
                  'cost', 'price', 'barcode', 'stock', 'tax_rate', 'price_adjust', 'printer',
                  'modifier_groups', 'active')
        widgets = {
            'sorting': forms.NumberInput(attrs={'max': 99999999, 'min': 0, 'required': True}),
            'cost': forms.NumberInput(attrs={'max': 99999999, 'min': 0, 'required': True}),
            'price': forms.NumberInput(attrs={'max': 99999999, 'min': 0, 'required': True}),
            'stock': forms.NumberInput(attrs={'max': 99999999, 'required': True}),
            'stock_change': forms.NumberInput(attrs={'max': 99999999}),
        }


class CvsUploadForm(forms.ModelForm):
    class Meta:
        model = Csv
        fields = ('group_csv',)


class QuickAddProductForm(forms.ModelForm):
    barcode = forms.CharField(max_length=255, required=False,widget=forms.TextInput(attrs={'placeholder': 'Enter barcode'}))
    name = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'placeholder': 'Enter Product Name'}))
    stock = forms.FloatField(required=False, widget=forms.TextInput(attrs={'placeholder': '0'}))
    price = forms.FloatField(required=False, widget=forms.TextInput(attrs={'placeholder': '0.00'}))

    def clean_barcode(self):
        form_data = super(QuickAddProductForm, self).clean()
        barcode = form_data['barcode']
        if form_data['barcode'] == "":
            return barcode
        products = Product.objects.filter(barcode=barcode)
        if products.count() > 0:
            raise forms.ValidationError(u'Item with this barcode already exists')
        # lets find this barcode
        return barcode

    class Meta:
        model = Product
        fields = ('barcode', 'name', 'stock', 'price', )


class ModifierForm(forms.ModelForm):
    group = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(
        attrs={
            'class': 'selectpicker modifier-creation-select',
            'multiple': 'multiple',
            'data-style': 'btn-secondary',
            'title': '',
        }),
        queryset=ModifierGroup.objects.all().exclude(archived=True))

    class Meta:
        model = Modifier
        fields = ('group', 'name', 'cost', 'price', 'active')
        help_texts = {
            'group': ''
        }
        widgets = {
            'cost': forms.NumberInput(attrs={'max': '99999999'}),
            'price': forms.NumberInput(attrs={'max': '99999999'})
        }


class CategoryForm(BaseProductCategory):
    color = forms.ChoiceField(choices=COLORS, widget=forms.RadioSelect)
    parent = forms.ModelChoiceField(queryset=Category.objects.all().exclude(archived=True), required=False)
    image = forms.ImageField(widget=FileImageWidget, required=False)

    class Meta:
        model = Category
        fields = ('name', 'parent', 'color', 'sorting', 'active', 'image', 'remove_photo')
        widgets = {
            'sorting': forms.NumberInput(attrs={'max': 1}),
            'active': forms.CheckboxInput(attrs={'data-plugin': 'switchery', 'data-color': '#5ac766'})
        }
