from django import forms
from .models import Customer, CustomerDocument

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['surname', 'first_name', 'nationality', 'gender']

class DocumentForm(forms.ModelForm):
    class Meta:
        model = CustomerDocument
        fields = ['customer', 'document_file']