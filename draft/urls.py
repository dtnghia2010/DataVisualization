from django.urls import path
from . import views


app_name = 'draft'
urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('options/', views.options, name='options'),
    path('results/', views.results, name='results'),
]
