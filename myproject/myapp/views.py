from django.shortcuts import render, redirect
from .models import CustomerDocument, Customer
from datetime import datetime
from django.contrib import messages
import json
import boto3


def upload_document(request):
    if request.method == 'POST' and request.FILES['document']:
        document = request.FILES['document']
        
        with open('uploaded_document.jpg', 'wb+') as destination:
            for chunk in document.chunks():
                destination.write(chunk)
        
        client = boto3.client('textract',region_name='',aws_access_key_id='',aws_secret_access_key='')
        with open('uploaded_document.jpg', 'rb') as image:
            img = bytearray(image.read())
        
        response = client.detect_document_text(Document={'Bytes': img})
        
        text = ""
        for item in response["Blocks"]:
            if item["BlockType"] == "LINE":
                text = text + " "+item["Text"]
                
        split_text = text.split('/')
        data = {}

        for item in split_text:
            pair = item.split(":")
            if len(pair) == 2:
                key = pair[0].strip()
                value = pair[1].strip()
                if key.lower() == "name":
                    name_parts = value.split()[:2]
                    value = ' '.join(name_parts)
                elif key.lower() == "dob":
                    dob_str = value.split()[0] 
                    dob = datetime.strptime(dob_str, '%d-%m-%Y')  
                    value = dob.strftime('%Y-%m-%d') 
                elif key.lower() == "you":
                    if "male" in value.lower():
                        gender = "Male"
                    elif "female" in value.lower():
                        gender = "Female"
                    else:
                        gender = "Unknown"
                    data["Gender"] = gender
                data[key] = value

        for item in split_text:
            item = item.strip()
            if item.lower().startswith("male") or item.lower().startswith("female"):
                gender_info = item.split()
                if "male" in item.lower():
                    data["Gender"] = "Male"
                elif "female" in item.lower():
                    data["Gender"] = "Female"
                
                aadhar_number = ' '.join([x for x in gender_info if x.isdigit() and len(x) == 4])
                if aadhar_number:
                    data["Aadhar Number"] = aadhar_number

        json_data = json.dumps(data)
        print(json_data)

        # Create or update Customer object based on extracted data
        customer, created = Customer.objects.update_or_create(
            customer_name=data.get('Name', ''),
            defaults={
                'dob': data.get('DOB', ''),
                'gender': data.get('Gender', ''),
                'aadhar_number': data.get('Aadhar Number', '') 
            }
        )

        # Create a CustomerDocument object and save extracted data
        customer_document = CustomerDocument.objects.create(
            customer_name=data.get('Name', ''),
            document_file=document,
            extracted_data=data
        )
        messages.success(request, "Document uploaded and processed successfully.")
        return redirect('customer_list')
    
    return render(request, 'upload.html')



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
