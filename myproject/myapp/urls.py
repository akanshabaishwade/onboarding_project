from django.urls import path
from .views import *

urlpatterns = [
    path('aws/upload/', upload_document, name='upload_document'),
    path('create_or_select_customer/', create_or_select_customer, name='create_or_select_customer'),
    path('customer_list/', customer_list, name='customer_list'),

]

