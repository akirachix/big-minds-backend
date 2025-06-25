from django.test import TestCase
from rest_framework.test import APIClient
from subscriptions.models import SubscriptionBox, ScheduledItem
from users.models import Buyer, Vendor
from product.models import Product
from rest_framework import status

class SubscriptionBoxAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.buyer = Buyer.objects.create(
            name="Test Buyer",
            password_hash="password",
            location="Test Location",
            phone_number="123456789"
        )
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            phone_number="987654321",
            password_hash="password",
            profile_picture=None,
            location="Vendor Location",
            shop_name="Vendor Shop",
            till_number=111222
        )
        self.product = Product.objects.create(
            name="Test Product",
            category="Fruits",
            product_image=None,
            unit="kg"
        )
        self.box = SubscriptionBox.objects.create(
            buyer=self.buyer,
            vendor=self.vendor,
            name="Fruit Box",
            frequency="monthly",
            price=29.99,
            status="active"
        )
        self.box_data = {
            "buyer": self.buyer.buyer_id,
            "vendor": self.vendor.vendor_id,
            "name": "Veggie Box",
            "frequency": "monthly",
            "price": "39.99",
            "status": "active"
        }
        self.scheduleditem_data = {
            "product": self.product.product_id,
            "schedule": self.box.schedule_id,
            "price_per_unit": "2.50",
            "quantity": 5,
            "unit": "kg"
        }

    
    def test_list_subscription_boxes(self):
        response = self.client.get("/api/subscriptions/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) >= 1)

    def test_create_subscription_box(self):
        response = self.client.post("/api/subscriptions/", self.box_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Veggie Box")

    def test_retrieve_subscription_box(self):
        response = self.client.get(f"/api/subscriptions/{self.box.schedule_id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], self.box.name)

    def test_delete_subscription_box(self):
        response = self.client.delete(f"/api/subscriptions/{self.box.schedule_id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(SubscriptionBox.objects.filter(schedule_id=self.box.schedule_id).exists())

    def test_create_scheduled_item(self):
        response = self.client.post("/api/scheduled-items/", self.scheduleditem_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["quantity"], 5)
        self.assertEqual(response.data["unit"], "kg")

    def test_list_scheduled_items(self):
        item = ScheduledItem.objects.create(
            product=self.product,
            schedule=self.box,
            price_per_unit=2.5,
            quantity=2,
            unit='kg'
        )
        response = self.client.get("/api/scheduled-items/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) >= 1)

    def test_retrieve_scheduled_item(self):
        item = ScheduledItem.objects.create(
            product=self.product,
            schedule=self.box,
            price_per_unit=2.5,
            quantity=2,
            unit='kg'
        )
        response = self.client.get(f"/api/scheduled-items/{item.scheduled_item_id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["quantity"], 2)

    def test_delete_scheduled_item(self):
        item = ScheduledItem.objects.create(
            product=self.product,
            schedule=self.box,
            price_per_unit=2.5,
            quantity=2,
            unit='kg'
        )
        response = self.client.delete(f"/api/scheduled-items/{item.scheduled_item_id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ScheduledItem.objects.filter(scheduled_item_id=item.scheduled_item_id).exists())