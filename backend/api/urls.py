
from django.shortcuts import render

# Create your views here.
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet
router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'order', OrderViewSet, basename='order')
urlpatterns = router.urls

