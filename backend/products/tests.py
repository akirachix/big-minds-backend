from django.test import TestCase
from users.models import Vendor
from .models import Product, VendorProduct

class ProductVendorProductModelTest(TestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(
            name="Nebyat",
            phone_number="254922442",
            password_hash="1010",
            location="karen",
            shop_name="Safi",
            till_number=123456
        )

        self.product = Product.objects.create(
            name="Banana",
            category="Fruits",
            product_image="mama_mboga.jpg",  
            unit="3k.g"
        )
        

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Banana")
        self.assertEqual(str(self.product), "Banana")

    def test_vendorproduct_creation(self):
        vendor_product = VendorProduct.objects.create(
            vendor=self.vendor,
            product=self.product,
            price=100.0,
            quantity=5,
            description="Fresh fruit"
        )
        self.assertEqual(vendor_product.price, 100.0)
        self.assertEqual(vendor_product.quantity, 5)
        self.assertEqual(str(vendor_product), f"{self.vendor} - {self.product}")

    def test_vendorproduct_relationship(self):
        vendor_product = VendorProduct.objects.create(
            vendor=self.vendor,
            product=self.product,
            price=200,
            quantity=10,
            description="Description"
        )
        self.assertEqual(vendor_product.vendor, self.vendor)
        self.assertEqual(vendor_product.product, self.product)
    