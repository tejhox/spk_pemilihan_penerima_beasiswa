from django.urls import path
from .views import *
 
app_name = 'SPK'

urlpatterns = [
    path('', index_view, name='index'),
    path('add/', add_view, name='add'),
    path('delete/<int:daftar_nim>', delete_view, name='delete'),
    path('kriteria/', kriteria_view, name='kriteria'),
    path('result/', tentukan_view, name='tentukan'),
    path('update/<int:daftar_nim>', update_view, name='update'),
    path('deleteall/', deleteAll, name='deleteall'),
]