from django import forms
from taskin.models import SpecialPrices


class TaskinSpecialPricesForm(forms.ModelForm):
    class Meta:
        model = SpecialPrices
        fields = ('product', 'price', 'group', 'archived')