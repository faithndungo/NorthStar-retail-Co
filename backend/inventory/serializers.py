# inventory/serializers.py

from rest_framework import serializers
from .models import Product, ProductVariant, StockAlert

class ProductVariantSerializer(serializers.ModelSerializer):
    is_in_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = ProductVariant
        fields = ['id', 'size', 'color', 'sku_variant', 'stock_quantity', 'is_in_stock']


class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'sku', 'description', 'price', 'variants']


class StockAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockAlert
        fields = ['id', 'variant', 'email', 'created_at']
        read_only_fields = ['id', 'created_at']