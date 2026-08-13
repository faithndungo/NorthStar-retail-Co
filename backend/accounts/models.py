import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class CustomerProfile(models.Model):
    # Optional link to a standard Django User (if registered)
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='profile'
    )
    # Unique token used for guest/anonymous session tracking from React
    session_token = models.UUIDField(
        default=uuid.uuid4, 
        unique=True, 
        editable=False
    )
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user:
            return f"User Profile: {self.user.username}"
        return f"Guest Profile ({self.email or self.session_token})"