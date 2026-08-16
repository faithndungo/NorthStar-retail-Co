from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.ReadOnlyField()
    name = serializers.CharField(source='product_variant.product.name', read_only=True)
    sku = serializers.CharField(source='product_variant.sku_variant', read_only=True)
    size = serializers.CharField(source='product_variant.size', read_only=True)
    color = serializers.CharField(source='product_variant.color', read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'order',
            'product_variant',
            'quantity',
            'unit_price',
            'subtotal',
            'name',
            'sku',
            'size',
            'color',
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'order_number',
            'customer',
            'status',
            'total_amount',
            'items',
            'created_at',
            'updated_at',
            'tracking_carrier',
            'tracking_url',
            'estimated_delivery',
        ]
        read_only_fields = fields
