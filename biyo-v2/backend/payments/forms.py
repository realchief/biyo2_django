from django import forms
from payments.models import Payment


class AddTipsForm(forms.Form):
    value = forms.DecimalField(required=True,)

