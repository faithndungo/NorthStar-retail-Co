from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            phone_number = serializer.validated_data.get('phone_number')

            #Look up existing profile by email if provided, or create a new guest profile

            if email:
                profile, created = CustomerProfile.objects.get_or_create(email=email, defaults={'phone_number': phone_number})
            else:
                profile = CustomerProfile.objects.create(phone_number=phone_number)

            profile_data = CustomerProfileSerializer(profile).data
            return Response({
                "message": "Session token retrieved successfully.",
                "data": profile_data
            },
            status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)