# inventory/admin.py

from django.contrib import admin
from .models import Product, ProductVariant, StockAlert

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ('size', 'color', 'sku_variant', 'stock_quantity')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sku', 'price', 'created_at')
    search_fields = ('name', 'sku')
    inlines = [ProductVariantInline]

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'size', 'color', 'sku_variant', 'stock_quantity', 'is_in_stock')
    list_filter = ('size', 'color')
    search_fields = ('product__name', 'sku_variant')

@admin.register(StockAlert)
class StockAlertAdmin(admin.ModelAdmin):
    list_display = ('id', 'variant', 'email', 'notified', 'created_at')
    list_filter = ('notified', 'created_at')
    search_fields = ('email', 'variant__product__name', 'variant__sku_variant')