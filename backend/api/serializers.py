from rest_framework import serializers
from .models import Product, VendorProduct
from users.models import Vendor

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_id', 'name', 'category', 'product_image', 'unit']

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['vendor_id', 'name']  

class VendorProductSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer(read_only=True)
    vendor_id = serializers.PrimaryKeyRelatedField(
        queryset=Vendor.objects.all(), source='vendor', write_only=True
    )
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )
    class Meta:
        model = VendorProduct
        fields = [
            'product_ddetails_id', 'vendor', 'vendor_id', 'product', 'product_id',
            'price', 'quantity', 'description', 'added_on', 'updated_at'
        ]
from cart.models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    # product_name = serializers.CharField(source="product.name", read_only=True)
    class Meta:
        model = CartItem
        fields ="__all__"

class CartSerializer(serializers.ModelSerializer):
    # items = CartItemSerializer(many=True, read_only=True)
    # customer_name = serializers.CharField(source="customer.name", read_only=True)
    class Meta:
        model = Cart
        fields ="__all__"

