# forms.py

from django import forms
from .models import Add_Data, Upload_File


class Add_DataFrom(forms.ModelForm):
    # Biểu mẫu cho dữ liệu về quốc gia và dân số
    class Meta:
        model = Add_Data
        fields = '__all__'


class Upload_FileForm(forms.ModelForm):
    # Biểu mẫu cho dữ liệu từ tệp CSV được tải lên
    class Meta:
        model = Upload_File
        fields = ['attribute1', 'attribute2']
