from django.db import models
from users.models import Buyer, Vendor
from product.models import Product




FREQUENCY_CHOICES = [
   ('weekly', 'Weekly'),
   ('monthly', 'Monthly'),
   ('Twice a week', 'twice a week'),
]
frequency = models.CharField( max_length=20, choices=FREQUENCY_CHOICES, default='monthly' )


class SubscriptionBox(models.Model):
  schedule_id = models.AutoField(primary_key=True)
#   buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='subscriptions')
#   vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='subscriptions')
  name = models.CharField(max_length=100)
  frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  start_date = models.DateTimeField(auto_now=True)
  status = models.CharField(max_length=100)




  def __str__(self):
      return f"Subscription {self.name} for {self.buyer.name}"






UNIT_CHOICES = [
  ('kg', 'Kg'),
  ('bunch', 'Bunch'),
 ]




class ScheduledItem(models.Model):
  scheduled_item_id = models.AutoField(primary_key=True)
#   product = models.ForeignKey(Product, on_delete=models.CASCADE)
#   schedule = models.ForeignKey(SubscriptionBox, on_delete=models.CASCADE, related_name='scheduled_items')
  price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
  quantity = models.IntegerField()
  unit = models.CharField(max_length=10, choices=UNIT_CHOICES)




  def __str__(self):
      return f"{self.quantity}{self.unit} {self.product.name} (Schedule {self.schedule.schedule_id})"


