from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('addBug', addBug, name='addBug'),
    path('record/', record, name='record'),
     path('delete_record/<int:ReporterID>/', views.delete_record, name='delete_record'),
    path('saveform', saveform, name='saveform'),
    path('fetch-records/', views.fetch_records_and_count_reporters, name='fetch_records_and_count_reporters'),
    path('update_record/<str:ReporterID>/',update_record,name='update_record')
]
