# Generated by Django 5.0.6 on 2024-05-22 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='surname',
        ),
        migrations.RemoveField(
            model_name='customerdocument',
            name='customer',
        ),
        migrations.AddField(
            model_name='customer',
            name='aadhar_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='customer_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='customerdocument',
            name='customer_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]