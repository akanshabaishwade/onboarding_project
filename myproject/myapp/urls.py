from django.urls import path
from .views import *

urlpatterns = [
    path('aws/upload/', upload_file, name='upload_document'),
    path('upload-success/', upload_success, name='upload_success'),
    # path('upload/', UploadDocumentView.as_view(), name='upload_document'),
    # path('document_uploaded/', DocumentUploadedView.as_view(), name='document_uploaded'),
]

