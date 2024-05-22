from django import forms
from .models import Customer, CustomerDocument

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['customer_name', 'gender']

class DocumentForm(forms.ModelForm):
    class Meta:
        model = CustomerDocument
        fields = ['customer_name', 'document_file']