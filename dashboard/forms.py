from django import forms
from .models import CountryData, UploadedFile
from .models import CountryData


class CountryDataFrom(forms.ModelForm):
    class Meta:
        model = CountryData
        fields='__all__'
class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']

