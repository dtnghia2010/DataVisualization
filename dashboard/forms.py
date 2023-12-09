from django import forms
from .models import CountryData, UploadedFile


class CountryDataFrom(forms.ModelForm):
    class Meta:
        model = CountryData
        fields = '__all__'


# forms.py
class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file', 'attribute1', 'attribute2']
