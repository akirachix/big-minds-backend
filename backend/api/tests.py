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


