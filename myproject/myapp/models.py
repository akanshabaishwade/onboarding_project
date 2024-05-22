from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class DocumentSet(models.Model):
    name = models.CharField(max_length=100)
    countries = models.ManyToManyField(Country)
    has_backside = models.BooleanField(default=False)
    ocr_labels = models.JSONField()

    def __str__(self):
        return self.name

class Customer(models.Model):
    surname = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    nationality = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    gender = models.CharField(max_length=10)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.surname}'


class CustomerDocument(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    document_file = models.FileField(upload_to='documents/')
    extracted_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Document for {self.customer}'

