# forms.py
# Name: 1
# Duong Trong Nghia ITITIU21256
# Ngo Thi Thuong ITCSIU21160
# Nguyen Pham Ky Phuong ITITIU21287
# Nguyen Anh Thang ITCSIU21233
# Purpose: Create forms to take the input.
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
