from django.test import TestCase
from users.models import Vendor, Buyer
from products.models import Product
from .models import Order, OrderItem
from decimal import Decimal

class OrderModelTest(TestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(
            name="Vendor1",
            phone_number="1234567890",
            password_hash="hashedpassword",
            location="Karen",
            shop_name="Vendor Shop",
            till_number=1001
        )
        self.buyer = Buyer.objects.create(
            name="Buyer1",
            password_hash="hashedpassword",
            location="Karen",
            phone_number="0987654321"
        )
        self.product = Product.objects.create(
            name="Mango",
            category="Fruit",
            unit="Bunch"
        )

    def test_order_creation(self):
        order = Order.objects.create(
            vendor=self.vendor,
            buyer=self.buyer,
            total_price=Decimal("150.50"),
            status="Pending"
        )
        self.assertIsInstance(order, Order)
        self.assertEqual(order.vendor, self.vendor)
        self.assertEqual(order.buyer, self.buyer)
        self.assertEqual(order.total_price, Decimal("150.50"))
        self.assertEqual(order.status, "Pending")
        self.assertEqual(str(order), f"Order {order.order_id}")

    def test_order_item_creation(self):
        order = Order.objects.create(
            vendor=self.vendor,
            buyer=self.buyer,
            total_price=Decimal("200.00"),
            status="Confirmed"
        )
        order_item = OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=3,
            price_at_order=Decimal("66.67")
        )
        self.assertIsInstance(order_item, OrderItem)
        self.assertEqual(order_item.order, order)
        self.assertEqual(order_item.product, self.product)
        self.assertEqual(order_item.quantity, 3)
        self.assertEqual(order_item.price_at_order, Decimal("66.67"))
        self.assertEqual(str(order_item), f"Item {order_item.item_id} in Order {order.order_id}")

    def test_cascade_delete_order_deletes_items(self):
        order = Order.objects.create(
            vendor=self.vendor,
            buyer=self.buyer,
            total_price=Decimal("300.00"),
            status="Pending"
        )
        order_item = OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=1,
            price_at_order=Decimal("300.00")
        )
        order.delete()
        self.assertFalse(OrderItem.objects.filter(pk=order_item.pk).exists())

    def test_cascade_delete_product_deletes_items(self):
        order = Order.objects.create(
            vendor=self.vendor,
            buyer=self.buyer,
            total_price=Decimal("400.00"),
            status="Pending"
        )
        order_item = OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=2,
            price_at_order=Decimal("200.00")
        )
        self.product.delete()
        self.assertFalse(OrderItem.objects.filter(pk=order_item.pk).exists())

