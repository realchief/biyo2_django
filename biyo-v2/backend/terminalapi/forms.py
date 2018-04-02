from django import forms
from products.models import Store


class PasswordProtectionForClearSales(forms.Form):
    login = forms.CharField(max_length=32, label='Store Name', widget=forms.PasswordInput,required=True)
    confirm_password = forms.CharField(max_length=32,label='Root Password', widget=forms.PasswordInput,required=True)

    def clean(self):
        cleaned_data = self.cleaned_data
        store = Store.objects.get(id=1)
        if self.cleaned_data.get('login') != store.name:
            raise forms.ValidationError('Wrong Store Name')
        if self.cleaned_data.get('confirm_password') != 'root':
            raise forms.ValidationError('Wrong password')
        else:
            return cleaned_data

