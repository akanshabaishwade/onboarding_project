from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CustomerModel, DocumentSetModel, CustomerDocumentModel
from .forms import CustomerForm, DocumentUploadForm
from django.conf import settings
import boto3
from google.cloud import vision


@login_required
def create_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.created_by = request.user
            customer.save()
            return redirect('list_customers')
    else:
        form = CustomerForm()
    return render(request, 'customer_form.html', {'form': form})

@login_required
def list_customers(request):
    customers = CustomerModel.objects.filter(created_by=request.user)
    return render(request, 'list_customers.html', {'customers': customers})

@login_required
def upload_document(request, customer_id):
    customer = CustomerModel.objects.get(id=customer_id)
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.customer = customer
            document.save()

            if settings.USE_AWS_TEXTRACT:
                # AWS Textract call
                client = boto3.client('textract')
                response = client.analyze_document(
                    Document={'S3Object': {'Bucket': 'your-bucket-name', 'Name': document.document_file.name}},
                    FeatureTypes=['TABLES', 'FORMS']
                )
                document.extracted_data = response
            else:
                # Google Cloud Vision API call
                client = vision.ImageAnnotatorClient()
                response = client.document_text_detection(image={'content': document.document_file.read()})
                document.extracted_data = response

            document.save()
            return redirect('list_customers')
    else:
        form = DocumentUploadForm()
    return render(request, 'upload_document.html', {'form': form, 'customer': customer})
