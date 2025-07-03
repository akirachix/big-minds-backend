from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet,SubscriptionBoxViewSet, ScheduledItemViewSet, PaymentViewSet, OrderViewSet, UserViewSet, OrderItemViewSet
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
from .views import (
    ProductViewSet, VendorProductViewSet, SubscriptionBoxViewSet, ScheduledItemViewSet, 
    PaymentViewSet, OrderViewSet, OrderItemViewSet, UserViewSet, CartViewSet, CartItemViewSet
)

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'vendor-products', VendorProductViewSet, basename='vendorproduct')
router.register(r'subscriptions', SubscriptionBoxViewSet, basename='subscriptionbox')
router.register(r'scheduled-items', ScheduledItemViewSet, basename='scheduleditem')
router.register(r'orders', OrderViewSet, basename='api_orders')
router.register(r'order-items', OrderItemViewSet, basename='order-items_api')
router.register(r'users', UserViewSet, basename='users_api')
router.register(r'payments', PaymentViewSet, basename='payments')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'cart-item', CartItemViewSet, basename='cart-item')

urlpatterns = [
    path('', include(router.urls)),
]


router.register(r'orders', OrderViewSet, basename='orders_api')
router.register(r'order-items', OrderItemViewSet, basename='api_order-items')


urlpatterns = [
    path('', include(router.urls)),
]