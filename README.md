# Django Onboarding Project

This Django project aims to extract data from PDF files stored in an AWS S3 bucket using Textract and Boto3 and post extract data to the Customer model.

## AWS Configuration

1. **AWS Account Setup**: Signed up for an AWS account and created an S3 bucket to store PDF files.

2. **Obtained AWS Credentials**: Retrieved AWS Access Key ID and Secret Access Key with the necessary permissions for S3 and Textract services.

3. **Added AWS Configuration**: Updated the Django settings file (`settings.py`) with the following AWS configuration:

    ```python
    # AWS Configuration
    AWS_S3_REGION_NAME = 'your-aws-region' 
    AWS_REGION = 'your-aws-region'  # Same as AWS_S3_REGION_NAME or different, depending on your setup
    AWS_ACCESS_KEY_ID = 'your-access-key-id'
    AWS_SECRET_ACCESS_KEY = 'your-secret-access-key'
    AWS_STORAGE_BUCKET_NAME = 'your-s3-bucket-name'
    ```
document link - https://docs.aws.amazon.com/code-library/latest/ug/python_3_textract_code_examples.html
## Screenshots

- Access key and Secret key generated:
![Access key and Secret key](https://github.com/akanshabaishwade/onboarding_project/assets/85228361/b39e9543-0711-4f46-af21-42d41801c56d)

- Document Upload:
![Sucessfully uploaded with massage](https://github.com/akanshabaishwade/onboarding_project/assets/85228361/72a0384b-0897-493b-817b-5725e110af4a)

- **Redirect to Customer List**: ![Redirect to Customer List](https://github.com/akanshabaishwade/onboarding_project/assets/85228361/cb8cf7f2-572a-4f2f-9dab-2eba5ef96607)

- **Surprit Kaur User Record Extracted by AWS Textract**:
- **Text Extraction**: User data extracted using AWS Textract from customer onboarding forms.
- **Update or Create Records**: Extracted data used to update existing records or create new records in the Customer model.
- **Create New Records**: When new data is uploaded, new records are created in the CustomerDocument model.

- **Solved Error**:
  - ![Error](https://github.com/akanshabaishwade/onboarding_project/assets/85228361/e9a5cf2b-a090-4028-b0d3-3c344e39f282)

- **Steps for Solving Error**:
  - **Generate a New Access Key**: Old key lacked necessary access permissions.
  - **Import boto3**: Use boto3 library.
  - **Create a New View**: Replace old code with new code for document processing.
  - **Use detect_document_text**: Utilize detect_document_text function for accurate text extraction.
  - **Create JSON Data**: Format extracted text into JSON as needed.
  - **Upload to Relevant Models**: Upload JSON data into appropriate database models.
  
- Customer Data Upload Form:
  ![Customer Data Upload Form](https://github.com/akanshabaishwade/onboarding_project/assets/85228361/efa4ae0a-8cd4-4254-bd97-8d9b0ed1c05f)

- After Posting Data Redirect:
  ![After Posting Data Redirect](https://github.com/akanshabaishwade/onboarding_project/assets/85228361/042676f9-6040-49f8-8a2a-6a79dea1dd6e)


