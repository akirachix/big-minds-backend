from django.db import models
from user.models import Vendor, Buyer
from products.models import Product

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='orders')
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100)
    order_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.order_id} by {self.buyer.name}"

class OrderedItem(models.Model):
    item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='ordered_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} in order {self.order.order_id}"