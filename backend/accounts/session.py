from rest_framework.exceptions import AuthenticationFailed

from .models import CustomerProfile


def get_session_profile(request, *, required=True):
    """Resolve the guest profile represented by X-Session-Token."""
    token = request.headers.get('X-Session-Token', '').strip()
    if not token:
        if required:
            raise AuthenticationFailed('A valid guest session is required.')
        return None

    try:
        return CustomerProfile.objects.get(session_token=token)
    except (CustomerProfile.DoesNotExist, ValueError):
        raise AuthenticationFailed('The guest session is invalid or expired.')
