# orders/serializers.py

from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    title = serializers.ReadOnlyField()
    sku = serializers.ReadOnlyField()
    subtotal = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
        fields = ['id', 'title', 'sku', 'quantity', 'unit_price', 'subtotal']


class OrderLookupSerializer(serializers.Serializer):
    order_number = serializers.CharField(required=True)
    customer_email = serializers.EmailField(required=True)


class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'order_number',
            'customer_email',
            'status',
            'carrier',
            'tracking_number',
            'tracking_url',
            'estimated_delivery',
            'total_amount',
            'items',
            'created_at',
        ]