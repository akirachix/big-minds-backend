from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, VendorProductViewSet


router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'vendor-products', VendorProductViewSet, basename='vendorproduct')


urlpatterns = [
   path('', include(router.urls)),
]
