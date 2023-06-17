from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('addBug', addBug, name='addBug'),
    path('record', record, name='record'),
    path('/record', record, name='/record'),
    path('delete_record/<str:ReporterID>/', delete_record, name='delete_record'),
    path('saveform', saveform, name='saveform'),
    path('update_record/<str:ReporterID>/',update_record,name='update_record')
]
