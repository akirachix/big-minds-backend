from rest_framework import viewsets
from products.models import Product, VendorProduct
from .serializers import ProductSerializer, VendorProductSerializer
from rest_framework.response import Response

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