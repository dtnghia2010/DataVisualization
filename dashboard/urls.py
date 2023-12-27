from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_data', views.add_data, name='add_data'),
    path('addData_algorithms', views.addData_algorithms, name='addData_algorithms'),
    path('upload_file', views.upload_file, name='upload_file'),
    path('uploadFile_algorithms', views.uploadFile_algorithms, name='uploadFile_algorithms'),
    # path('upload_sort', views.upload_sort, name='upload_sort'),
    path('sorting/Upload', views.processingUpload, name='sortUp'),
    path('sorting/Add', views.processingAdd, name='sortAdd'),
    path('delete_add_data', views.delete_add_data, name='delete_add_data'),
    path('search_page_upload', views.search_page_upload, name='search_page_upload'),
    path('search_add_data/', views.search_add_data, name='search_add_data')
    path('predict_data', views.predict_data, name='predict_data'),
]


