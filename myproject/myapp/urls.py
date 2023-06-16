from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('addBug', addBug, name='addBug'),
    path('record', record, name='record'),
    path('record', record, name='record'),
    path('delete/<str:record_id>/', delete_record, name='delete_record'),
    path('saveform', saveform, name='saveform'),
]
