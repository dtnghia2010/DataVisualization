from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_data', views.add_data, name='add_data'),
    path('upload_file', views.upload_file, name='upload_file'),
    path('sorting/Upload', views.processingUpload, name='sortUp'),
    path('sorting/Add', views.processingAdd, name='sortAdd')
]


