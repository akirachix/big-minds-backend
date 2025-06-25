from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubscriptionBoxViewSet
from .views import ScheduledItemViewSet

router=DefaultRouter()
router.register(r"subscriptions", SubscriptionBoxViewSet, basename="subscriptionbox")
router.register(r"scheduled-items", ScheduledItemViewSet, basename="scheduleditem")

urlpatterns = [
    path("",include(router.urls)),
]
