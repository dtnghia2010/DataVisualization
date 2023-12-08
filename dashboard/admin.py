from django.contrib import admin
from . models import CountryData, UploadedFile

# Register your models here.
admin.site.register(CountryData)
admin.site.register(UploadedFile)