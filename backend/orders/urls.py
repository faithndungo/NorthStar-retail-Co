# orders/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderItemViewSet, OrderLookupView, OrderDetailByNumberView

router = DefaultRouter()
router.register('manage', OrderViewSet, basename='order-manage')
router.register('items-manage', OrderItemViewSet, basename='order-item-manage')

urlpatterns = [
    path('lookup/', OrderLookupView.as_view(), name='order-lookup'),
    path('<str:order_number>/', OrderDetailByNumberView.as_view(), name='order-detail-by-number'),
    path('', include(router.urls)),
]