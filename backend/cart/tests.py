from django.test import TestCase
from django.utils import timezone
from users.models import Buyer
from products.models import Product
from .models import Cart, CartItem

class CartModelTest(TestCase):
    def setUp(self):
        self.buyer = Buyer.objects.create(
            name='Helen',
            password_hash='testword',
            location='Nairobi',
            phone_number='123456789'
        )
        self.product = Product.objects.create(
            name='Asha',
            category='Fruit',
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
        self.assertTrue(isinstance(self.cart.added_at, timezone.datetime))
        self.assertEqual(str(self.cart), f"Cart {self.cart.cart_id} for {self.buyer.name}")

    def test_cartitem_creation(self):
        self.assertEqual(self.cart_item.cart, self.cart)
        self.assertEqual(self.cart_item.product, self.product)
        self.assertEqual(self.cart_item.quantity, 3)
        self.assertTrue(isinstance(self.cart_item.added_at, timezone.datetime))
        self.assertEqual(
            str(self.cart_item),
            f"3x {self.product.name} in Cart {self.cart.cart_id}"
        )

    def test_cartitem_relationship(self):
        self.assertIn(self.cart_item, self.cart.cartitem_set.all())

    def test_cart_multiple_items(self):
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
        self.assertEqual(self.cart.cartitem_set.count(), 2)
        self.assertIn(cart_item2, self.cart.cartitem_set.all())