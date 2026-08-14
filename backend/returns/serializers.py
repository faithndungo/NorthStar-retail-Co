from rest_framework import serializers
from .models import Return, ReturnItem


class ReturnItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnItem
        fields = [
            'id',
            'return_request',
            'order_item',
            'quantity',
        ]


class ReturnSerializer(serializers.ModelSerializer):
    items = ReturnItemSerializer(many=True, read_only=True)

    class Meta:
        model = Return
        fields = [
            'id',
            'order',
            'reason',
            'status',
            'items',
            'created_at',
            'updated_at',
        ]