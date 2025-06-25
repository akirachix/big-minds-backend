

# Create your tests here.
from django.test import TestCase
from .models import Vendor, Buyer
from django.db import IntegrityError

class VendorModelTest(TestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(
            name="Vendor One",
            phone_number="0700000000",
            password_hash="hashedpassword",
            location="Kigali",
            shop_name="Shop One",
            till_number=123456,
        )

    def test_vendor_creation(self):
        self.assertEqual(self.vendor.name, "Vendor One")
        self.assertEqual(self.vendor.till_number, 123456)
        self.assertIsNotNone(self.vendor.created_at)
        self.assertIsNotNone(self.vendor.last_login)

    def test_unique_till_number(self):
        with self.assertRaises(IntegrityError):
            Vendor.objects.create(
                name="Vendor Two",
                phone_number="0711111111",
                password_hash="anotherhash",
                location="Huye",
                shop_name="Shop Two",
                till_number=123456,  # Same as previous: should raise error
            )

    def test_str_representation(self):
        self.assertEqual(str(self.vendor), "Vendor One")

class BuyerModelTest(TestCase):
    def setUp(self):
        self.buyer = Buyer.objects.create(
            name="Buyer One",
            password_hash="hashedpassword2",
            location="Musanze",
            phone_number="0799999999",
        )

    def test_buyer_creation(self):
        self.assertEqual(self.buyer.name, "Buyer One")
        self.assertEqual(self.buyer.location, "Musanze")
        self.assertIsNotNone(self.buyer.created_at)
        self.assertIsNotNone(self.buyer.last_login)

    def test_str_representation(self):
        self.assertEqual(str(self.buyer), "Buyer One")