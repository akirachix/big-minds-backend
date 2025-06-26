from rest_framework import viewsets
from products.models import Product, VendorProduct
from .serializers import ProductSerializer, VendorProductSerializer
from rest_framework.response import Response
from subscription.models import SubscriptionBox, ScheduledItem
from .serializers import SubscriptionBoxSerializer, ScheduledItemSerializer
from django.shortcuts import render
from orders.models import Order, OrderItem
from .serializers import OrderSerializers, OrderItemSerializer
from users.models import User
from .serializers import UserSerializer
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class VendorProductViewSet(viewsets.ModelViewSet):
    queryset = VendorProduct.objects.all()
    serializer_class = VendorProductSerializer

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        print("Current vendor products:", queryset)  
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class SubscriptionBoxViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionBox.objects.all()
    serializer_class = SubscriptionBoxSerializer

class ScheduledItemViewSet(viewsets.ModelViewSet):
    queryset = ScheduledItem.objects.all()
    serializer_class = ScheduledItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['type']  
    search_fields = ['name', 'phone_number', 'location', 'shop_name']
