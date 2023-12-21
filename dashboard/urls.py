from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_data', views.add_data, name='add_data'),
    path('addData_algorithms', views.addData_algorithms, name='addData_algorithms'),
    path('upload_file', views.upload_file, name='upload_file'),
    path('uploadFile_algorithms', views.uploadFile_algorithms, name='uploadFile_algorithms'),
    path('upload_sort', views.upload_sort, name='upload_sort')]
