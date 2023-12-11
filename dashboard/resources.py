from import_export import resources
from .models import Upload_File


class UploadedFileResource(resources.ModelResource):
    class Meta:
        model = Upload_File
