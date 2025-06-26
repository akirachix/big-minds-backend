from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from users.models import Vendor
from products.models import Product, VendorProduct
import tempfile
import os

@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            phone_number="123456789",
            password_hash="somerandomhash",
            location="Test Location",
            shop_name="Test Shop",
            till_number=1001,
        )
        self.product = Product.objects.create(
            name="Test Product",
            category="Test Category",
            product_image="https://example.com/test.jpg",  # Use a valid URL
            unit="kg"
        )
        self.vendor_product = VendorProduct.objects.create(
            vendor=self.vendor,
            product=self.product,
            price=10.0,
            quantity=5,
            description="Test vendor product"
        )

    def tearDown(self):
        # No need to delete files, since product_image is a URL
        pass

    def test_api_root(self):
        response = self.client.get(reverse('api-root'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('products', response.data)
        self.assertIn('vendor-products', response.data)

    def test_product_list(self):
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        if isinstance(data, dict):
            results = data.get('results', data)
        else:
            results = data
        self.assertGreaterEqual(len(results), 1)
        self.assertEqual(results[0]['name'], self.product.name)

    def test_product_create(self):
        data = {
            "name": "Another Product",
            "category": "Another Category",
            "product_image": "https://example.com/image.jpg",  
            "unit": "pcs"
        }
        response = self.client.post(reverse('product-list'), data, format='json')
        if response.status_code != status.HTTP_201_CREATED:
            print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(response.data['name'], "Another Product")

    def test_product_detail(self):
        response = self.client.get(reverse('product-detail', args=[self.product.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name)

    def test_vendor_product_list(self):
        response = self.client.get(reverse('vendorproduct-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        if isinstance(data, dict):
            results = data.get('results', data)
        else:
            results = data
        self.assertGreaterEqual(len(results), 1)
        self.assertEqual(results[0]['description'], self.vendor_product.description)

    def test_vendor_product_create(self):
        product = Product.objects.create(
            name="New Product",
            category="Category",
            product_image="https://example.com/another.jpg", 
            unit="pcs"
        )
        data = {
            "vendor": self.vendor.pk,
            "product": product.pk,
            "price": 20.0,
            "quantity": 10,
            "description": "Another vendor product"
        }
        response = self.client.post(reverse('vendorproduct-list'), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(VendorProduct.objects.count(), 2)
        self.assertEqual(response.data['description'], "Another vendor product")

    def test_vendor_product_detail(self):
        response = self.client.get(reverse('vendorproduct-detail', args=[self.vendor_product.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], self.vendor_product.description)