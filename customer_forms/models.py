from django.contrib.auth.models import AbstractUser
from django.db import models

class CountryModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    country = models.ForeignKey(CountryModel, on_delete=models.SET_NULL, null=True, blank=True)

class DocumentSetModel(models.Model):
    document_name = models.CharField(max_length=100)
    countries = models.ManyToManyField(CountryModel)
    has_backside = models.BooleanField(default=False)
    ocr_labels = models.JSONField()

    def __str__(self):
        return self.document_name

class CustomerModel(models.Model):
    surname = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    nationality = models.ForeignKey(CountryModel, on_delete=models.SET_NULL, null=True)
    gender = models.CharField(max_length=10)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.surname}"

class CustomerDocumentModel(models.Model):
    customer = models.ForeignKey(CustomerModel, on_delete=models.CASCADE)
    document_file = models.FileField(upload_to='documents/')
    extracted_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document for {self.customer}"
