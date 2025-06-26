from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, VendorProductViewSet
from .views import SubscriptionBoxViewSet, ScheduledItemViewSet
from .views import OrderViewSet, OrderItemViewSet
from .views import UserViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'vendor-products', VendorProductViewSet, basename='vendorproduct')


urlpatterns = [
   path('', include(router.urls)),
]


router = DefaultRouter()
router.register(r'subscriptions', SubscriptionBoxViewSet, basename='subscriptionbox')
router.register(r'scheduled-items', ScheduledItemViewSet, basename='scheduleditem')

router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'order-items',OrderItemViewSet, basename='order-items')

router.register(r'users', UserViewSet)

urlpatterns = router.urls
