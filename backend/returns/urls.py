from django.urls import path

from .views import ReturnEligibilityView, ReturnRequestView


urlpatterns = [
    path('returns/eligibility/', ReturnEligibilityView.as_view(), name='return-eligibility'),
    path('returns/requests/', ReturnRequestView.as_view(), name='return-request'),
]
