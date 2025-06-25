from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import Vendor, Buyer
from product.models import Product
from order.models import Order, OrderItem

class OrderAPITests(APITestCase):
    def setUp(self):
        # Create Vendor
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            phone_number="1234567890",
            password_hash="hashedpassword",
            location="Nairobi",
            shop_name="Vendor Shop",
            till_number=1001,
        )
        # Create Buyer
        self.buyer = Buyer.objects.create(
            name="Test Buyer",
            password_hash="hashedpassword",
            location="Nairobi",
            phone_number="0987654321",
        )
        # Create Product
        self.product = Product.objects.create(
            name="Test Product",
            category="Groceries",
            unit="kg",
        )
        # Create Order
        self.order = Order.objects.create(
            vendor=self.vendor,
            buyer=self.buyer,
            total_price=200.00,
            status="Pending"
        )
        # Create OrderItem
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price_at_order=100.00
        )

    def test_list_orders(self):
        url = reverse('orders-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_create_order(self):
        url = reverse('orders-list')
        data = {
            "vendor": self.vendor.pk,
            "buyer": self.buyer.pk,
            "total_price": 300.00,
            "status": "Confirmed"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["total_price"], "300.00")

    def test_retrieve_order(self):
        url = reverse('orders-detail', args=[self.order.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["order_id"], self.order.pk)

    def test_update_order(self):
        url = reverse('orders-detail', args=[self.order.pk])
        data = {
            "vendor": self.vendor.pk,
            "buyer": self.buyer.pk,
            "total_price": 250.00,
            "status": "Shipped"
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "Shipped")

    def test_delete_order(self):
        url = reverse('orders-detail', args=[self.order.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(pk=self.order.pk).exists())


class OrderItemAPITests(APITestCase):
    def setUp(self):
        # Create Vendor, Buyer, Product, Order
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            phone_number="1234567890",
            password_hash="hashedpassword",
            location="Nairobi",
            shop_name="Vendor Shop",
            till_number=1002,
        )
        self.buyer = Buyer.objects.create(
            name="Test Buyer",
            password_hash="hashedpassword",
            location="Nairobi",
            phone_number="0987654322",
        )
        self.product = Product.objects.create(
            name="Milk",
            category="Dairy",
            unit="litre",
        )
        self.order = Order.objects.create(
            vendor=self.vendor,
            buyer=self.buyer,
            total_price=150.00,
            status="Pending"
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            price_at_order=150.00
        )

    def test_list_order_items(self):
        url = reverse('order-items-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_create_order_item(self):
        url = reverse('order-items-list')
        data = {
            "order": self.order.pk,
            "product": self.product.pk,
            "quantity": 3,
            "price_at_order": 300.00
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["quantity"], 3)

    def test_retrieve_order_item(self):
        url = reverse('order-items-detail', args=[self.order_item.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["item_id"], self.order_item.pk)

    def test_update_order_item(self):
        url = reverse('order-items-detail', args=[self.order_item.pk])
        data = {
            "order": self.order.pk,
            "product": self.product.pk,
            "quantity": 5,
            "price_at_order": 750.00
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["quantity"], 5)

    def test_delete_order_item(self):
        url = reverse('order-items-detail', args=[self.order_item.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(OrderItem.objects.filter(pk=self.order_item.pk).exists())