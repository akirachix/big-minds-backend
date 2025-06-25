from rest_framework.routers import DefaultRouter
from .views import VendorViewSet, BuyerViewSet

router = DefaultRouter()
router.register(r'vendors', VendorViewSet, basename='vendor')
router.register(r'buyers', BuyerViewSet, basename='buyer')

urlpatterns = router.urls