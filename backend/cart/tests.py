from django.test import TestCase

from user.models import Buyer
from products.models import Product
from cart.models import Cart, CartItem

class CartModelTest(TestCase):
    def setUp(self):
        self.buyer = Buyer.objects.create(
            name='Test Buyer',
            password_hash='testpassword',
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
            cart=self.cart,
            product=self.product,
            quantity=3
        )

    def test_cart_creation(self):
        self.assertEqual(self.cart.customer, self.buyer)
        self.assertEqual(str(self.cart), f"Cart {self.cart.cart_id} for {self.buyer.name}")

    def test_cartitem_creation(self):
        self.assertEqual(self.cart_item.cart, self.cart)
        self.assertEqual(self.cart_item.product, self.product)
        self.assertEqual(self.cart_item.quantity, 3)
        self.assertEqual(str(self.cart_item),
                         f"3x {self.product.name} in Cart {self.cart.cart_id}")

    def test_cartitem_relationship(self):
        # Test reverse relationship from Cart to CartItem
        self.assertIn(self.cart_item, self.cart.items.all())

    def test_cart_multiple_items(self):
        # Add another item to the same cart
        product2 = Product.objects.create(
            name='Test Product 2',
            category='Test Category',
            product_image='test2.jpg',
            unit='pcs'
        )
        cart_item2 = CartItem.objects.create(
            cart=self.cart,
            product=product2,
            quantity=1
        )
        self.assertEqual(self.cart.items.count(), 2)
        self.assertIn(cart_item2, self.cart.items.all())


# Create your tests here.

