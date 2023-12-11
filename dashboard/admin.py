from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Add_Data, Upload_File

# Register your models here.
admin.site.register(Add_Data)
admin.site.register(Upload_File)


class UploadedFileAdmin(ImportExportModelAdmin):
    list_display = ('Country Name', 'Country Code', 'Year 2022')
