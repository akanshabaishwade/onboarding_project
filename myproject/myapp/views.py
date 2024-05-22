from django.shortcuts import render, redirect
from .forms import DocumentForm
from .models import CustomerDocument, Customer
import boto3
from botocore.exceptions import ClientError
from django.contrib import messages
import os
from django.shortcuts import render, redirect
from .models import Customer, CustomerDocument, Country
from django.conf import settings


def extract_data_from_s3(bucket, document):
    client = boto3.client('textract')
    response = client.analyze_document(
        Document={'S3Object': {'Bucket': bucket, 'Name': document}},
        FeatureTypes=['FORMS']
    )

    kvs = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET' and block['EntityTypes'][0] == 'KEY':
            key = ''
            value = ''
            for relationship in block['Relationships']:
                if relationship['Type'] == 'VALUE':
                    value_block_id = relationship['Ids'][0]
                    value_block = next(
                        item for item in response['Blocks'] if item['Id'] == value_block_id)
                    if 'Text' in value_block:
                        value = value_block['Text']
            if 'Text' in block:
                key = block['Text']
            kvs[key] = value

    return kvs


def upload_file(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)

            s3_client = boto3.client('s3', region_name=settings.AWS_REGION)
            try:
                file_contents = request.FILES['document_file'].read()

                s3_client.put_object(
                    Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                    Key=document.document_file.name,
                    Body=file_contents
                )

                extracted_data = extract_data_from_s3(
                    settings.AWS_STORAGE_BUCKET_NAME, document.document_file.name)

                if extracted_data:
                    document.extracted_data = extracted_data
                else:
                    document.extracted_data = "No data extracted"

                document.save()

                messages.success(request, 'File uploaded successfully.')

                return redirect('upload_success')
            except ClientError as e:
                error_message = f"Error uploading file to S3: {e}"
                return render(request, 'upload.html', {'form': form, 'error_message': error_message})
    else:
        form = DocumentForm()
    return render(request, 'upload.html', {'form': form})


def upload_success(request):
    return render(request, 'upload_success.html')


def extracted_data(request, customer):
    get_data = CustomerDocument.objects.filter(customer=customer)
    post_data = Customer.objects.filter(customer=customer)


# ------------------------------------------------------------------------------------------------
# from django.shortcuts import render, redirect
# from django.views import View
# from .forms import DocumentForm
# import fitz  # PyMuPDF
# import json

# class UploadDocumentView(View):
#     def get(self, request):
#         form = DocumentForm()
#         return render(request, 'upload.html', {'form': form})

#     def post(self, request):
#         form = DocumentForm(request.POST, request.FILES)
#         if form.is_valid():
#             document = form.save(commit=False)
#             document.file_name = request.FILES['document_file'].name  # Save the file name

#             # Process the uploaded PDF with PyMuPDF
#             extracted_data = self.extract_data_from_pdf(document.document_file.path)

#             # Update the document with extracted data
#             document.extracted_data = extracted_data
#             document.save()

#             return redirect('document_uploaded')  # Redirect to a success page
#         return render(request, 'upload.html', {'form': form})

#     def extract_data_from_pdf(self, pdf_path):
#         pdf_document = fitz.open(pdf_path)
#         pdf_text = ""
#         for page_num in range(pdf_document.page_count):
#             page = pdf_document[page_num]
#             pdf_text += page.get_text()
#         pdf_document.close()

#         # Convert text to JSON
#         text_json = {'text': pdf_text}
#         return json.dumps(text_json)

# class DocumentUploadedView(View):
#     def get(self, request):
#         return render(request, 'document_uploaded.html')



def create_or_select_customer(request):
    if request.method == 'POST':
        customer_name = request.POST.get('existing_customer')

        if not customer_name:  
            customer_name = request.POST.get('customer_name')
            dob = request.POST.get('dob')
            gender = request.POST.get('gender')
            aadhar_number = request.POST.get('aadhar_number')
            Customer.objects.create(
                customer_name=customer_name, dob=dob, gender=gender, aadhar_number=aadhar_number)
        else:
            customer_document = CustomerDocument.objects.filter(
                customer_name=customer_name).first()
            if customer_document:
                extracted_data = customer_document.extracted_data

                if isinstance(extracted_data, dict):
                    dob = extracted_data.get('dob')
                    gender = extracted_data.get('gender')
                    aadhar_number = extracted_data.get('aadhar_number')

                    Customer.objects.create(
                        customer_name=customer_name, dob=dob, gender=gender, aadhar_number=aadhar_number)
                else:
                    pass

        return redirect('customer_list')

    customer_names = CustomerDocument.objects.values_list(
        'customer_name', flat=True).distinct()

    return render(request, 'create_or_select_customer.html', {'customer_names': customer_names})


def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customer_list.html', {'customers': customers})
