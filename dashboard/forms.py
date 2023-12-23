# forms.py

from django import forms
from .models import Add_Data, Upload_File


class Add_DataFrom(forms.ModelForm):
    # Biểu mẫu cho dữ liệu của add_data
    class Meta:
        model = Add_Data
        fields = '__all__'


class Upload_FileForm(forms.ModelForm):
    # Biểu mẫu cho dữ liệu từ tệp CSV được tải lên
    class Meta:
        model = Upload_File
        fields = ['attribute1', 'attribute2']


ALGORITHM_CHOICES = [
    ('quicksort', 'quicksort'),
]

class sortingForm(forms.Form):
    algorithm = forms.CharField(label='Selected algorithm', widget=forms.Select(choices=ALGORITHM_CHOICES))