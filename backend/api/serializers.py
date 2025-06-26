from rest_framework import serializers
from products.models import Product, VendorProduct

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class VendorProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorProduct
        fields = '__all__'
from subscription.models import SubscriptionBox, ScheduledItem
from orders.models import Order, OrderItem
from users.models import User

class SubscriptionBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionBox
        fields = "__all__"

class ScheduledItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledItem
        fields = "__all__"


class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
