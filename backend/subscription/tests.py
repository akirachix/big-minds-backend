
from django.test import TestCase
from subscription.models import SubscriptionBox, ScheduledItem
from users.models import Buyer, Vendor
from products.models import Product


class SubscriptionBoxModelTest(TestCase):
   def setUp(self):
    
       self.buyer = Buyer.objects.create(
           name="Test Buyer",
           password_hash="pw",
           location="loc",
           phone_number="123"
       )
       self.vendor = Vendor.objects.create(
           name="Test Vendor",
           phone_number="987",
           password_hash="pw",
           profile_picture=None,
           location="Vendor Loc",
           shop_name="Shop",
           till_number=12345
       )
       self.product = Product.objects.create(
           name="Banana",
           category="Fruit",
           product_image=None,
           unit="kg"
       )


   def test_subscription_box_creation(self):
       box = SubscriptionBox.objects.create(
           buyer=self.buyer,
           vendor=self.vendor,
           name="My Box",
           frequency="monthly",
           price=10.50,
           status="active"
       )
       self.assertEqual(box.name, "My Box")
       self.assertEqual(box.frequency, "monthly")
       self.assertEqual(box.price, 10.50)
       self.assertEqual(box.status, "active")
       self.assertEqual(box.buyer, self.buyer)
       self.assertEqual(box.vendor, self.vendor)
       self.assertTrue(str(box).startswith("Subscription My Box for"))


   def test_scheduled_item_creation(self):
       box = SubscriptionBox.objects.create(
           buyer=self.buyer,
           vendor=self.vendor,
           name="Test Box",
           frequency="weekly",
           price=25.00,
           status="active"
       )
       item = ScheduledItem.objects.create(
           product=self.product,
           schedule=box,
           price_per_unit=3.25,
           quantity=2,
           unit="kg"
       )
       self.assertEqual(item.product, self.product)
       self.assertEqual(item.schedule, box)
       self.assertEqual(item.price_per_unit, 3.25)
       self.assertEqual(item.quantity, 2)
       self.assertEqual(item.unit, "kg")
       self.assertIn("Banana", str(item))
       self.assertIn("2kg", str(item))


   def test_subscription_box_with_items(self):
       box = SubscriptionBox.objects.create(
           buyer=self.buyer,
           vendor=self.vendor,
           name="Fruit Box",
           frequency="Twice a week",
           price=30.00,
           status="pending"
       )
       ScheduledItem.objects.create(
           product=self.product,
           schedule=box,
           price_per_unit=5.00,
           quantity=1,
           unit="bunch"
       )
       self.assertEqual(box.scheduled_items.count(), 1)