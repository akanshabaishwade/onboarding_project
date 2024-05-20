from django.urls import path
from .views import create_customer, list_customers, upload_document
from django.contrib.auth import views as auth_views

app_name = 'customer_forms' 

urlpatterns = [
    path('create-customer/', create_customer, name='create_customer'),
    path('list-customers/', list_customers, name='list_customers'),
    path('upload-document/<int:customer_id>/', upload_document, name='upload_document'),
        path('accounts/custom-login/', auth_views.LoginView.as_view(template_name='login.html'), name='custom_login'),
]
