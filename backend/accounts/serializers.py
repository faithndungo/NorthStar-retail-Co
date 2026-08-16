from rest_framework import serializers
from .models import CustomerProfile

class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = ['id', 'session_token', 'email', 'phone_number', 'created_at']
        read_only_fields = ['id', 'session_token', 'created_at']

class SessionInitSerializer(serializers.Serializer):
    """
    Serializer used when client requests/initializes a session token
    """
    email = serializers.EmailField(required=False, allow_blank=True)
    phone_number = serializers.CharField(required=False, allow_blank=True, max_length=20)
    session_token = serializers.UUIDField(required=False)
