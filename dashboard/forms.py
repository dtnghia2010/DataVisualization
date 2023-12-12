from django import forms
from .models import Add_Data, Upload_File


class Add_DataFrom(forms.ModelForm):
    class Meta:
        model = Add_Data
        fields = '__all__'



class Upload_FileForm(forms.ModelForm):
    class Meta:
        model = Upload_File
        fields = ['attribute1', 'attribute2']
