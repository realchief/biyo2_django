from django import forms
from django.utils.translation import ugettext_lazy as _

from employees.models import Employee, Customer
from products.models import Terminal


class EmployeeFilterForm(forms.Form):
    employees = forms.ModelChoiceField(label='', help_text="",queryset=Employee.objects.all().exclude(archived=True), required=True)
    # date_range = forms.CharField(max_length=100, initial='Click to choose date...')


class CustomerPaymentForm(forms.Form):
    """
    Form for issuing payment to customers' orders
    """

    PAYMENT_METHOD_CHOICES = [
        ("Cash", "Cash"),
        ("Check", "Check"),
        ("Creditcard", "Credit Card"),
        ("Account", "Account")
    ]

    customer = forms.ModelChoiceField(queryset=Customer.objects.exclude(archived=True), widget=forms.Select(attrs={
        'type': "text", 'class': "form-control"}))
    amount = forms.DecimalField(widget=forms.NumberInput(attrs={'class': "form-control"}))
    payment_method = forms.ChoiceField(label=_("Payment Method"), choices=PAYMENT_METHOD_CHOICES, widget=forms.Select(
        attrs={'type': "text", 'class': "form-control"}))
    payment_date = forms.DateTimeField(input_formats=("%m-%d-%Y %I:%M %p",), label=_("Date"), widget=forms.DateTimeInput(
        attrs={'class': "form-control"}))
    check_number = forms.CharField(label=_("Check #"), max_length=15, required=False, widget=forms.TextInput(
        attrs={'class': "form-control"}))

    def clean(self):
        payment_method = self.cleaned_data.get("payment_method")
        check_number = self.cleaned_data.get("check_number")
        if payment_method == "check" and not check_number:
            raise forms.ValidationError(_("Check number is required for this payment method."))


class ReportsSortForm(forms.Form):
    # date_range = forms.CharField(max_length=100, initial='Today', help_text="")
    employees = forms.ModelChoiceField(label="", help_text="", widget=forms.Select(attrs={'class': 'form-control select2-hidden-accessible',
                                                                                          'data-plugin': "select2",
                                                                                          'data-allow-clear': "true",
                                                                                          'tabindex': "-1",
                                                                                          'aria-hidden': "true"}),
                                       empty_label='All Employees',
                                       queryset=Employee.objects.all().exclude(archived=True), required=False, )
    terminal = forms.ModelChoiceField(label="", help_text="", widget=forms.Select(attrs={'class': 'form-control select2-hidden-accessible',
                                                                                          'data-plugin': "select2",
                                                                                          'data-allow-clear': "true",
                                                                                          'tabindex': "-1",
                                                                                          'aria-hidden': "true"}),
                                       empty_label='All Terminals',
                                       queryset=Terminal.objects.all().exclude(archived=True), required=False)

    def __init__(self, request, *args, **kwargs):
        super(ReportsSortForm, self).__init__(*args, **kwargs)
        self.fields["employees"].initial = request.session.get('employee')
        self.fields["terminal"].initial = request.session.get('terminal')
