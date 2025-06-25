from rest_framework import viewsets
from .models import Payment
from .serializers import PaymentSerializer
from .models import Order
from .serializers import OrderSerializer
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer