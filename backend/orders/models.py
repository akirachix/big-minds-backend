from django.db import models
from users.models import User
from product.models import Product
from django.db.models import Sum,F
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vendor_orders', limit_choices_to={'type':'vendor'})
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_orders', limit_choices_to={'type':'customer'})
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable = False)
    status = models.CharField(max_length=100)
    order_date = models.DateTimeField(auto_now_add=True)

    def update_total_price(self):
        total=self.orderitem_set.aggregate(
            total=Sum(F('quantity') * F('price_at_order'))
        )['total'] or 0
        self.total_price = total
        self.save()

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