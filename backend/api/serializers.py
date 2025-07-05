from rest_framework import serializers
from product.models import Product, VendorProduct
from users.models import User
from payment.models import Payment
from subscription.models import SubscriptionBox, ScheduledItem
from orders.models import Order, OrderItem
from cart.models import Cart, CartItem




class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_id', 'name', 'category', 'product_image', 'unit']

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'name']

class VendorProductSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer(read_only=True)
    vendor_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(type='vendor'), source='vendor', write_only=True
    )
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = VendorProduct
        fields = [
            'product_details_id', 'vendor', 'vendor_id', 'product', 'product_id',
            'price', 'quantity', 'description', 'added_on', 'updated_at'
        ]

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_name = serializers.CharField(write_only=True)
    customer_name = serializers.CharField(write_only=True)
    cart_item_id = serializers.IntegerField(read_only=True)
    quantity = serializers.IntegerField()
    added_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = CartItem
        fields = ['cart_item_id', 'product', 'product_name', 'customer_name', 'quantity', 'added_at']
        read_only_fields = ['cart_item_id', 'product', 'added_at']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer.")
        return value

    def validate_product_name(self, value):
        try:
            product = Product.objects.get(name=value)
            return product
        except Product.DoesNotExist:
            raise serializers.ValidationError(f"Product with name '{value}' not found.")
        except Product.MultipleObjectsReturned:
            raise serializers.ValidationError(
                f"Multiple products found with name '{value}'. Please use a unique identifier."
            )

    def validate_customer_name(self, value):
        try:
            user = User.objects.get(name=value, type='customer')
            return user
        except User.DoesNotExist:
            raise serializers.ValidationError(f"Customer with name '{value}' not found or not a customer.")
        except User.MultipleObjectsReturned:
            raise serializers.ValidationError(
                f"Multiple customers found with name '{value}'. Please use a unique identifier."
            )

    def create(self, validated_data):
        product = validated_data['product_name']
        quantity = validated_data['quantity']
        customer = validated_data['customer_name']

        if isinstance(product, str):
            product = Product.objects.get(name=product)
        if isinstance(customer, str):
            customer = User.objects.get(name=customer, type='customer')

        cart, _ = Cart.objects.get_or_create(customer=customer)
        cart_item, created = CartItem.objects.get_or_create(
            cart_id=cart, product=product, defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        return cart_item

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(write_only=True, required=False)
    customer_id = serializers.IntegerField(write_only=True, required=False)
    cart_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cart
        fields = ['cart_id', 'items', 'customer_name', 'customer_id', 'created_at']
        read_only_fields = ['cart_id', 'items', 'created_at']

    def validate(self, data):
        customer_name = data.get('customer_name')
        customer_id = data.get('customer_id')

        if not customer_name and not customer_id:
            raise serializers.ValidationError("One of 'customer_name' or 'customer_id' must be provided.")

        user = None
        if customer_name and customer_id:
            try:
                user = User.objects.get(name=customer_name, user_id=customer_id, type='customer')
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    f"No customer found with name '{customer_name}' and user_id '{customer_id}'."
                )
        elif customer_name:
            try:
                user = User.objects.get(name=customer_name, type='customer')
            except User.DoesNotExist:
                raise serializers.ValidationError(f"Customer with name '{customer_name}' not found or not a customer.")
            except User.MultipleObjectsReturned:
                raise serializers.ValidationError(
                    f"Multiple customers found with name '{customer_name}'. Please provide 'customer_id' for clarity."
                )
        else:
            try:
                user = User.objects.get(user_id=customer_id, type='customer')
            except User.DoesNotExist:
                raise serializers.ValidationError(f"Customer with user_id '{customer_id}' not found or not a customer.")

        if Cart.objects.filter(customer=user).exists():
            raise serializers.ValidationError(f"Customer with name '{user.name}' or user_id '{user.user_id}' already has a cart.")

        data['customer'] = user
        return data

    def create(self, validated_data):
        customer = validated_data.pop('customer')
        validated_data.pop('customer_name', None)
        validated_data.pop('customer_id', None)
        try:
            cart = Cart.objects.create(customer=customer)
            return cart
        except ValueError as e:
            raise serializers.ValidationError(str(e))

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['cart_id'] = instance.cart_id
        representation['customer_name'] = instance.customer.name if instance.customer else None
        representation['customer_id'] = instance.customer.user_id if instance.customer else None
        return representation

class MpesaPaymentSerializer(serializers.Serializer):
     class Meta:
        model = Payment
        fields = '__all__'

class STKPushSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    account_reference = serializers.CharField()
    transaction_desc = serializers.CharField()

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'payment_id', 'order', 'method', 'status', 'amount',
            'merchant_request_id', 'checkout_request_id', 'result_code',
            'result_desc', 'mpesa_receipt_number', 'phone_number',
            'transaction_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['payment_id', 'created_at', 'updated_at']

class SubscriptionBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionBox
        fields = '__all__'

class ScheduledItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledItem
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset = Product.objects.all(),
        source = 'product',
        write_only=True
    )
    class Meta:
        model = OrderItem
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)
    vendor_name = serializers.CharField(source='vendor.name', read_only=True)
    buyer_name = serializers.CharField(source='buyer.name', read_only=True)
    total_price = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    class Meta:
        model = Order
        fields = "__all__"

