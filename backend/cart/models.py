from django.db import models
from user.models import Buyer
from products.models import Product

class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='carts')
    added_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.cart_id} for {self.customer.name}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    added_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} in Cart {self.cart.cart_id}"