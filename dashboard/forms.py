# forms.py

from django import forms
from .models import Add_Data, Upload_File


class Add_DataFrom(forms.ModelForm):
    # Biểu mẫu cho dữ liệu của add_data
    class Meta:
        model = Add_Data
        fields = '__all__'


class DeleteForm_AddData(forms.Form):
    items_to_delete = forms.ModelMultipleChoiceField(queryset=Add_Data.objects.all(),
                                                     widget=forms.CheckboxSelectMultiple)


class Upload_FileForm(forms.ModelForm):
    # Biểu mẫu cho dữ liệu từ tệp CSV được tải lên
    class Meta:
        model = Upload_File
        fields = ['attribute1', 'attribute2']


class nameChart(forms.Form):
    name = forms.CharField(max_length=100)