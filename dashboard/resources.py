from import_export import resources
from .models import UploadedFile


class UploadedFileResource(resources.ModelResource):
    class Meta:
        model = UploadedFile
