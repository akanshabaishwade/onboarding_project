# Generated by Django 5.0.6 on 2024-05-22 19:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_customer_dob'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='nationality',
        ),
    ]
