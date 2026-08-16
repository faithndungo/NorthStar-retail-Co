from django.urls import path

from .views import OrderLookupView


urlpatterns = [
    path('orders/lookup/', OrderLookupView.as_view(), name='order-lookup'),
]
