from django import forms
from .models import CustomerModel, CustomerDocumentModel

class CustomerForm(forms.ModelForm):
    class Meta:
        model = CustomerModel
        fields = ['surname', 'first_name', 'nationality', 'gender']

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = CustomerDocumentModel
        fields = ['document_file']
