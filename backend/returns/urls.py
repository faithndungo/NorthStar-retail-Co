# returns/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReturnViewSet, ReturnItemViewSet, ReturnEligibilityView, ReturnRequestCreateView

router = DefaultRouter()
router.register('manage', ReturnViewSet, basename='return-manage')
router.register('items-manage', ReturnItemViewSet, basename='return-item-manage')

urlpatterns = [
    path('eligibility/', ReturnEligibilityView.as_view(), name='return-eligibility'),
    path('requests/', ReturnRequestCreateView.as_view(), name='return-request-create'),
    path('', include(router.urls)),
]