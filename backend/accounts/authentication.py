# accounts/authentication.py

from rest_framework.authentication import BaseAuthentication
from .models import CustomerProfile

class SessionTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('X-Session-Token')
        if not token:
            return None  # Anonymous request

        try:
            profile = CustomerProfile.objects.get(session_token=token)
            return (profile, token)  # Attaches profile as request.user
        except (CustomerProfile.DoesNotExist, ValueError):
            return None