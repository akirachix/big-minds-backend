
from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from users.models import Vendor
from .models import Product, VendorProduct
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image
import tempfile

def get_temporary_image():
    image = Image.new('RGB', (100, 100), color = 'red')
    tmp_file = BytesIO()
    image.save(tmp_file, 'jpeg')
    tmp_file.seek(0)
    return SimpleUploadedFile('test.jpg', tmp_file.read(), content_type='image/jpeg')

@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.image = get_temporary_image()
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
            product_image=self.image,
            unit="kg"
        )
        self.vendor_product = VendorProduct.objects.create(
            vendor=self.vendor,
            product=self.product,
            price=10.0,
            quantity=5,
            description="Test vendor product"
        )

    def test_api_root(self):
        response = self.client.get(reverse('api-root'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('products', response.data)
        self.assertIn('vendor-products', response.data)

    def test_product_list(self):
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_product_create(self):
        image = get_temporary_image()
        data = {
            "name": "Another Product",
            "category": "Another Category",
            "product_image": image,
            "unit": "pcs"
        }
        response = self.client.post(reverse('product-list'), data, format='multipart')
        print("Product create response:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_product_detail(self):
        response = self.client.get(reverse('product-detail', args=[self.product.product_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name)

    def test_vendor_product_list(self):
        response = self.client.get(reverse('vendorproduct-list'))
        print("VendorProduct list response:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_vendor_product_create(self):
        product = Product.objects.create(
            name="New Product",
            category="Category",
            product_image=self.image,
            unit="pcs"
        )
        data = {
            "vendor_id": self.vendor.vendor_id,
            "product_id": product.product_id,
            "price": 20.0,
            "quantity": 10,
            "description": "Another vendor product"
        }
        response = self.client.post(reverse('vendorproduct-list'), data, format="json")
        print("VendorProduct create response:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(VendorProduct.objects.count(), 2)

    def test_vendor_product_detail(self):
        response = self.client.get(reverse('vendorproduct-detail', args=[self.vendor_product.product_ddetails_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], self.vendor_product.desc
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from user.models import Buyer
from products.models import Product
from cart.models import Cart, CartItem

class CartAPITestCase(APITestCase):
    def setUp(self):
      
        self.buyer = Buyer.objects.create(
            name='Test Buyer',
            password_hash='hashedpw',
            location='Test City',
            phone_number='123456789'
        )
        self.product = Product.objects.create(
            name='Test Product',
            category='Test Category',
            product_image='test.jpg',
            unit='kg'
        )
        self.cart = Cart.objects.create(customer=self.buyer)
        self.cart_item = CartItem.objects.create(
            cart=self.cart, product=self.product, quantity=2
        )

    def test_create_cart(self):
        url = reverse('cart-list')
        data = {
            "customer": self.buyer.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cart.objects.count(), 2)

    def test_get_cart_list(self):
        url = reverse('cart-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Cart.objects.count())

    def test_retrieve_cart(self):
        url = reverse('cart-detail', kwargs={'pk': self.cart.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['cart_id'], self.cart.cart_id)

    def test_update_cart(self):
        url = reverse('cart-detail', kwargs={'pk': self.cart.pk})
        data = {
            "customer": self.buyer.pk,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['customer'], self.buyer.pk)

    def test_delete_cart(self):
        url = reverse('cart-detail', kwargs={'pk': self.cart.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Cart.objects.filter(pk=self.cart.pk).exists())

class CartItemAPITestCase(APITestCase):
    def setUp(self):
        self.buyer = Buyer.objects.create(
            name='Test Buyer',
            password_hash='hashedpw',
            location='Test City',
            phone_number='123456789'
        )
        self.product = Product.objects.create(
            name='Test Product',
            category='Test Category',
            product_image='test.jpg',
            unit='kg'
        )
        self.cart = Cart.objects.create(customer=self.buyer)
        self.cart_item = CartItem.objects.create(
            cart=self.cart, product=self.product, quantity=2
        )

    def test_create_cart_item(self):
        url = reverse('cartitem-list')
        data = {
            "cart": self.cart.pk,
            "product": self.product.pk,
            "quantity": 3
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartItem.objects.count(), 2)

    def test_get_cartitem_list(self):
        url = reverse('cartitem-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), CartItem.objects.count())

    def test_retrieve_cart_item(self):
        url = reverse('cartitem-detail', kwargs={'pk': self.cart_item.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['cart'], self.cart.pk)

    def test_update_cart_item(self):
        url = reverse('cartitem-detail', kwargs={'pk': self.cart_item.pk})
        data = {
            "cart": self.cart.pk,
            "product": self.product.pk,
            "quantity": 10
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quantity'], 10)

    def test_delete_cart_item(self):
        url = reverse('cartitem-detail', kwargs={'pk': self.cart_item.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CartItem.objects.filter(pk=self.cart_item.pk).exists())

