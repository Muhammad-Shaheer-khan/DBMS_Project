from django.urls import path
from . import views
from .views import *
from django.urls import reverse
ReporterID = "abc123"


urlpatterns = [
    path('', home, name='home'),
    path('addBug', addBug, name='addBug'),
    path('record/', record, name='record'),
    path('delete_record/<str:ReporterID>/', delete_record, name='delete_record'),
    path('saveform', saveform, name='saveform'),
    # path('fetch_records/', fetch_records, name='fetch_records'),
    path('update_record/<str:ReporterID>/',update_record,name='update_record'),
]
