from django.db import models
from users.models import Vendor, Buyer
from products.models import Product 



class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    vendor = models.ForeignKey(Vendor, on_delete = models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete = models.CASCADE)
    total_price = models.DecimalField(max_digits = 10, decimal_places = 2)
    status = models.CharField(max_length = 100)
    order_date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"Order {self.order_id}"
    
class OrderItem(models.Model):
    item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Item {self.item_id} in Order {self.order.order_id}"
