# accounts/admin.py

from django.contrib import admin
from .models import CustomerProfile

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'phone_number', 'session_token', 'created_at')
    search_fields = ('email', 'phone_number', 'session_token')
    readonly_fields = ('session_token', 'created_at', 'updated_at')
    ordering = ('-created_at',)