from django import forms
from . import models


class SearchForm(forms.Form):
    name = forms.CharField(required=False)
    min_price = forms.IntegerField(required=False, min_value=1)
    max_price = forms.IntegerField(required=False, min_value=1)
    in_stock = forms.BooleanField(required=False)
