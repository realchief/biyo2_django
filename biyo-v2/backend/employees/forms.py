from django import forms

from employees.models import Employee, Customer, CsvCustomer, Supplier
from products.forms import FileImageWidget
from taskin.models import CustomerGroup


class ChangeEmpPass(forms.Form):
    old_password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                    'id': "inputPassword",
                                                                                    'name': "old_password",
                                                                                    'placeholder': "Old Password"}),
                                   required=True)
    new_password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                    'id': "inputPassword",
                                                                                    'name': "password",
                                                                                    'placeholder': "Password"}),
                                   required=True)
    confirm_password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                        'id': "passwordCheck",
                                                                                        'name': "confirm_password",
                                                                                        'placeholder': "Confirm Password"}),
                                       required=True)

    def clean(self):
        cleaned_data = self.cleaned_data
        if self.cleaned_data.get('new_password') != self.cleaned_data.get('confirm_password'):
            raise forms.ValidationError('The new passwords must be same')
        else:
            return cleaned_data


class EmployeeCreateForm(forms.ModelForm):
    password = forms.CharField(max_length=32, widget=forms.PasswordInput, required=False)
    email = forms.EmailField(required=False)
    photo = forms.ImageField(widget=FileImageWidget, required=False)

    class Meta:
        model = Employee
        fields = (
            'email', 'password', 'name', 'photo', 'address', 'address2', 'city', 'state',
            'zipcode', 'phone', 'pin', 'hourly_rate', 'role', 'store'
        )

        # def clean_email(self):
        #
        #     if not (self.cleaned_data.get('email', '')):
        #         self.cleaned_data.get('email', 'rrr')
        #
        #     return self.cleaned_data.get('email', '')
        # def clean(self):
        #     cleaned_data = self.cleaned_data
        #     if self.cleaned_data.get('password')=='':
        #         raise forms.ValidationError('Bla bla')
        #     else:
        #         return cleaned_data
        # def save(self, commit=True,*args, **kwargs):
        #     data=super(EmployeeCreateForm, self).save(*args, **kwargs)
        #     # data = self.cleaned_data
        #     if data.password=='':
        #         from random import randrange
        #         password=hashers.make_password(randrange(1000))
        #         print password
        #         data.password=password
        #
        #     if data.email=='':
        #         data.email='test@test.ru'
        #     if commit:
        #         data.save()
        #     return data


class EmployeeForm(forms.ModelForm):
    password = forms.CharField(max_length=32, widget=forms.PasswordInput, required=True)
    photo = forms.ImageField(widget=FileImageWidget, required=False)

    class Meta:
        model = Employee
        exclude = ('password',)
        fields = (
            'email', 'name', 'photo', 'address', 'address2', 'city', 'state',
            'zipcode', 'phone', 'pin', 'hourly_rate', 'role', 'store'
        )

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['password'] = forms.CharField(max_length=32, widget=forms.PasswordInput, required=False)
            # del self.fields['password']
            # else:
            #     del self.fields['password']


class CustomerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['rewards_points'].widget.attrs['readonly'] = True
        self.fields['group'].queryset = self.fields['group'].queryset.exclude(archived=True).order_by('name')

    class Meta:
        model = Customer
        exclude = ('profile_key',)


class AddCustomerForm(forms.ModelForm):
    def __init__(self, *args, **kwards):
        super(AddCustomerForm, self).__init__(*args, **kwards)
        self.fields['rewards_points'].widget.attrs['readonly'] = True
        self.fields['group'].queryset = self.fields['group'].queryset.exclude(archived=True).order_by('name')

    class Meta:
        model = Customer
        exclude = ('profile_key', 'archived')
        widgets = {
            'notes': forms.TextInput()
        }


class TaskinGroupForm(forms.ModelForm):
    class Meta:
        model = CustomerGroup
        exclude = ('archive',)


class CvsCustomerUploadForm(forms.ModelForm):
    class Meta:
        model = CsvCustomer
        fields = ('group_csv',)


######################Supplier###########################

class SupplierForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SupplierForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Supplier
        exclude = ('archived',)
        widgets = {
            'description': forms.Textarea(attrs={'resize': 'none'}),
            'default_markup': forms.NumberInput(attrs={'max': 999999999})
        }


class AddSupplierForm(forms.ModelForm):
    def __init__(self, *args, **kwards):
        super(AddSupplierForm, self).__init__(*args, **kwards)

    class Meta:
        model = Supplier
        exclude = ('archived',)
        widgets = {
            'description': forms.Textarea(
                            attrs={'rows': 5,
                                   'style': 'height: 100px;'}),
            'default_markup': forms.NumberInput(attrs={'max': 999999999})
        }

