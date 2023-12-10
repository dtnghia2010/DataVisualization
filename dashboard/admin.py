from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import CountryData, UploadedFile

# Register your models here.
admin.site.register(CountryData)
admin.site.register(UploadedFile)


class UploadedFileAdmin(ImportExportModelAdmin):
    list_display = ('Country', 'Population')
