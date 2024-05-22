from django.contrib import admin
from .models import Country, DocumentSet, Customer, CustomerDocument

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(DocumentSet)
class DocumentSetAdmin(admin.ModelAdmin):
    list_display = ('name', 'has_backside')
    filter_horizontal = ('countries',)
    search_fields = ('name', 'countries__name')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'gender', 'aadhar_number')
    search_fields = ('customer_name',)
    list_filter = ('gender', 'aadhar_number')


@admin.register(CustomerDocument)
class CustomerDocumentAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'created_at')
    date_hierarchy = 'created_at'
