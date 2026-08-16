from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import CustomerProfile
from .serializers import CustomerProfileSerializer, SessionInitSerializer

# Create your views here.
class SessionTokenView(APIView):
    """
    POST /api/accounts/session/
    initializes or fetches a guest CustomerProfile session token
    """

    def post(self, request):
        serializer = SessionInitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data.get('session_token')
        email = serializer.validated_data.get('email') or None
        phone_number = serializer.validated_data.get('phone_number') or None

        profile = None
        created = False
        if token:
            profile = CustomerProfile.objects.filter(session_token=token).first()

        if profile is None:
            profile = CustomerProfile.objects.create(
                email=email,
                phone_number=phone_number,
            )
            created = True
        else:
            changed = False
            if email and not profile.email:
                profile.email = email
                changed = True
            if phone_number and not profile.phone_number:
                profile.phone_number = phone_number
                changed = True
            if changed:
                profile.save()

        profile_data = CustomerProfileSerializer(profile).data
        return Response(
            {
                "message": "Session token created." if created else "Session token retrieved.",
                "session_token": str(profile.session_token),
                "data": profile_data,
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )
    permission_classes = [AllowAny]
