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


class CustomerDocumentInline(admin.TabularInline):
    model = CustomerDocument
    readonly_fields = ('extracted_data',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'surname', 'nationality', 'gender', 'created_by')
    search_fields = ('first_name', 'surname', 'nationality__name')
    list_filter = ('nationality', 'gender')
    inlines = [CustomerDocumentInline]


@admin.register(CustomerDocument)
class CustomerDocumentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'created_at')
    search_fields = ('customer__first_name', 'customer__surname')
    date_hierarchy = 'created_at'
