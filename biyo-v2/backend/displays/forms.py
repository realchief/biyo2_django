from django import forms

from displays.models import Box, Display


class BoxForm(forms.ModelForm):
    hidden_field = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Box
        exclude = ('archived', 'element')

    background_color = forms.CharField(max_length=7, widget=forms.TextInput(attrs={'data-type': 'minicolors'}))

    def __init__(self, *args, **kwargs):
        super(BoxForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['hidden_field'].initial = self.instance.pk


class DisplayForm(forms.ModelForm):
    class Meta:
        model = Display
        exclude = ('archived',)

    background_color = forms.CharField(max_length=7, widget=forms.TextInput(attrs={'data-type': 'minicolors'}))
