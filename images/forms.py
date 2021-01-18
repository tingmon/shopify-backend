from django import forms
from . import models


class SearchForm(forms.Form):
    name = forms.CharField(required=False)
    min_price = forms.IntegerField(required=False, min_value=1)
    max_price = forms.IntegerField(required=False, min_value=1)
    in_stock = forms.BooleanField(required=False)


class PhotoDeleteForm(forms.Form):
    delete = forms.BooleanField(required=False)


class PhotoAddForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = (
            "caption",
            "file",
        )

    def save(self, pk, *args, **kwargs):
        photo = super().save(commit=False)
        product = models.Product.objects.get(pk=pk)
        photo.product = product
        photo.save()
