from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_data', views.add_data, name='add_data'),
    path('upload_file', views.upload_file, name='upload_file'),
    path('upload_sort', views.upload_sort, name='upload_sort'),
    path('predict_data', views.predict_data, name='predict_data'),
]
