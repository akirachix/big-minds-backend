from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import User
from product.models import Product, VendorProduct
from cart.models import Cart, CartItem
from subscription.models import SubscriptionBox, ScheduledItem
from orders.models import Order, OrderItem
from payment.models import Payment
from decimal import Decimal

class ProductAPITest(APITestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Apple", category="Fruit", product_image="https://img.com/apple.jpg", unit="kg"
        )

    def test_list_products(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_product(self):
        url = reverse('product-list')
        data = {
            "name": "Banana",
            "category": "Fruit",
            "product_image": "https://img.com/banana.jpg",
            "unit": "kg"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), 2)

    def test_retrieve_product(self):
        url = reverse('product-detail', args=[self.product.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], "Apple")

class VendorProductAPITest(APITestCase):
    def setUp(self):
        self.vendor = User.objects.create(
            name="Vendor1", phone_number="0700000000", password_hash="hash",
            location="Loc", shop_name="S1", till_number=123, type="vendor"
        )
        self.product = Product.objects.create(
            name="Banana", category="Fruit", product_image="img.com/banana.jpg", unit="kg"
        )
        self.vendor_product = VendorProduct.objects.create(
            vendor=self.vendor, product=self.product, price=10.0, quantity=20, description="Yellow bananas"
        )

    def test_list_vendor_products(self):
        url = reverse('vendorproduct-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_vendor_product(self):
        url = reverse('vendorproduct-list')
        data = {
            "vendor_id": self.vendor.pk,
            "product_id": self.product.pk,
            "price": 20.0,
            "quantity": 15,
            "description": "Ripe Bananas"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(VendorProduct.objects.count(), 2)

class SubscriptionBoxAPITest(APITestCase):
    def setUp(self):
        self.buyer = User.objects.create(
            name="Buyer", phone_number="0700000033", password_hash="h", location="Loc", type="customer"
        )
        self.vendor = User.objects.create(
            name="Vendor", phone_number="0700000044", password_hash="h", location="Loc", type="vendor", till_number=123, shop_name="Shop"
        )

    def test_create_subscription_box(self):
        url = reverse('subscriptionbox-list')
        data = {
            "buyer": self.buyer.pk,
            "vendor": self.vendor.pk,
            "name": "Monthly Fruits",
            "frequency": "monthly",
            "price": 100,
            "status": "active"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(SubscriptionBox.objects.count(), 1)

class ScheduledItemAPITest(APITestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Kiwi", category="Fruit", product_image="img.com/kiwi.jpg", unit="kg"
        )
        self.buyer = User.objects.create(
            name="Buyer", phone_number="0700000033", password_hash="h", location="Loc", type="customer"
        )
        self.vendor = User.objects.create(
            name="Vendor", phone_number="0700000044", password_hash="h", location="Loc", type="vendor", till_number=123, shop_name="Shop"
        )
        self.box = SubscriptionBox.objects.create(
            buyer=self.buyer, vendor=self.vendor, name="Box", frequency="weekly", price=50, status="active"
        )

    def test_create_scheduled_item(self):
        url = reverse('scheduleditem-list')
        data = {
            "product": self.product.pk,
            "schedule": self.box.pk,
            "price_per_unit": 5.0,
            "quantity": 3,
            "unit": "kg"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ScheduledItem.objects.count(), 1)

class OrderAPITest(APITestCase):
    def setUp(self):
        self.vendor = User.objects.create(
            name="Vendor", phone_number="0700000044", password_hash="h", location="Loc", type="vendor", till_number=123, shop_name="Shop"
        )
        self.buyer = User.objects.create(
            name="Buyer", phone_number="0700000033", password_hash="h", location="Loc", type="customer"
        )

    def test_create_order(self):
        url = reverse('orders-list')
        data = {
            "vendor": self.vendor.pk,
            "buyer": self.buyer.pk,
            "total_price": 60.0,
            "status": "Pending"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Order.objects.count(), 1)

class OrderItemAPITest(APITestCase):
    def setUp(self):
        self.vendor = User.objects.create(
            name="Vendor", phone_number="0700000044", password_hash="h", location="Loc", type="vendor", till_number=123, shop_name="Shop"
        )
        self.buyer = User.objects.create(
            name="Buyer", phone_number="0700000033", password_hash="h", location="Loc", type="customer"
        )
        self.product = Product.objects.create(
            name="Melon", category="Fruit", product_image="img.com/melon.jpg", unit="kg"
        )
        self.order = Order.objects.create(
            vendor=self.vendor, buyer=self.buyer, total_price=40.0, status="Confirmed"
        )

    def test_create_order_item(self):
        url = reverse('order-items-list')
        data = {
            "order": self.order.pk,
            "product_id": self.product.pk,
            "quantity": 4,
            "price_at_order": 10.0
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(OrderItem.objects.count(), 1)

class UserAPITest(APITestCase):
    def test_create_user(self):
        url = reverse('users_api-list')
        data = {
            "name": "NewUser",
            "phone_number": "0711111111",
            "password_hash": "pw",
            "location": "Loc",
            "type": "customer"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)

    def test_list_users(self):
        User.objects.create(
            name="UserA", phone_number="0799999999", password_hash="pw", location="Loc", type="vendor"
        )
        url = reverse('users_api-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

class PaymentAPITest(APITestCase):
    def setUp(self):
        self.vendor = User.objects.create(
            name="Vendor", phone_number="0700000044", password_hash="h", location="Loc", type="vendor", till_number=123, shop_name="Shop"
        )
        self.buyer = User.objects.create(
            name="Buyer", phone_number="0700000033", password_hash="h", location="Loc", type="customer"
        )
        self.product = Product.objects.create(
            name="Apple", category="Fruit", product_image="img.com/apple.jpg", unit="kg"
        )
        self.order = Order.objects.create(
            vendor=self.vendor, buyer=self.buyer, total_price=100.00, status="pending"
        )
        self.payment = Payment.objects.create(
            order=self.order,
            method="M-Pesa",
            status="pending",
            amount="100.00",
            merchant_request_id="merchant123",
            checkout_request_id="checkout123"
        )

    def test_create_payment(self):
        url = reverse('payments-list')
        data = {
            "order": self.order.pk,
            "method": "M-Pesa",
            "status": "pending",
            "amount": "100.00",
            "merchant_request_id": "merchantABC",
            "checkout_request_id": "checkoutABC",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Payment.objects.count(), 2)
        payment = Payment.objects.get(merchant_request_id="merchantABC")
        self.assertEqual(payment.amount, self.order.total_price)
        self.assertEqual(payment.status, "pending")

    def test_list_payments(self):
        url = reverse('payments-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertIn("merchant123", [p["merchant_request_id"] for p in response.data])

    def test_retrieve_payment(self):
        url = reverse('payments-detail', args=[self.payment.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["payment_id"], self.payment.pk)
        self.assertEqual(response.data["merchant_request_id"], "merchant123")

    def test_update_payment(self):
        url = reverse('payments-detail', args=[self.payment.pk])
        data = {
            "status": "success"
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        self.payment.refresh_from_db()
        self.assertEqual(self.payment.status, "success")

    def test_full_update_payment(self):
        url = reverse('payments-detail', args=[self.payment.pk])
        new_order = Order.objects.create(
            vendor=self.vendor, buyer=self.buyer, total_price=150.00, status="pending"
        )
        data = {
            "order": new_order.pk,
            "method": "Card",
            "status": "failed",
            "amount": "150.00",
            "merchant_request_id": "merchantX",
            "checkout_request_id": "checkoutX"
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 200)
        self.payment.refresh_from_db()
        self.assertEqual(self.payment.order.pk, new_order.pk)
        self.assertEqual(self.payment.status, "failed")
        self.assertEqual(self.payment.amount, new_order.total_price)

    def test_delete_payment(self):
        url = reverse('payments-detail', args=[self.payment.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Payment.objects.filter(pk=self.payment.pk).exists())

    def test_create_payment_missing_required(self):
        url = reverse('payments-list')
        data = {
            # missing merchant_request_id, which is required
            "order": self.order.pk,
            "method": "M-Pesa",
            "status": "pending",
            "amount": "100.00",
            "checkout_request_id": "uniqueY"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("merchant_request_id", response.data)

    def test_create_payment_duplicate_merchant(self):
        url = reverse('payments-list')
        data = {
            "order": self.order.pk,
            "method": "M-Pesa",
            "status": "pending",
            "amount": "100.00",
            "merchant_request_id": "merchant123",  # already exists
            "checkout_request_id": "uniqueZ"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("merchant_request_id", response.data)

class CartAPITest(APITestCase):
    def setUp(self):
        self.customer = User.objects.create(
            name="CartUser", phone_number="0777777777", password_hash="pw", location="Loc", type="customer"
        )

    def test_create_cart(self):
        url = reverse('cart-list')
        data = {"customer_name": self.customer.name}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Cart.objects.count(), 1)

class CartItemAPITest(APITestCase):
    def setUp(self):
        self.customer = User.objects.create(
            name="ItemUser", phone_number="0788888888", password_hash="pw", location="Loc", type="customer"
        )
        self.cart = Cart.objects.create(customer=self.customer)
        self.product = Product.objects.create(
            name="Grape", category="Fruit", product_image="img.com/grape.jpg", unit="kg"
        )

    def test_create_cart_item(self):
        url = reverse('cart-item-list')
        data = {
            "product_name": self.product.name,
            "customer_name": self.customer.name,
            "quantity": 2
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(CartItem.objects.count(), 1)

