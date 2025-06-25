from rest_framework import serializers
from cart.models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="products.name", read_only=True)
    class Meta:
        model = CartItem
        fields ="__all__"

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source="customer.name", read_only=True)
    class Meta:
        model = Cart
        fields ="__all__"