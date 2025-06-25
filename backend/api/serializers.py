from rest_framework import serializers
from .models import Payment
from order.models import Order
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'  # Or specify fields you want
class PaymentSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    order_id = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(), source='order', write_only=True
    )
    payment_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Payment
        fields = ['payment_id', 'order', 'order_id', 'method', 'status', 'amount']





