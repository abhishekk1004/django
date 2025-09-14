from django.contrib import admin
from .models import Product

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'category', 'price', 'stock', 'quantity', 'updated_at')
    list_filter = ('category',)
    search_fields = ('sku', 'name', 'description')
    ordering = ('-updated_at',)
