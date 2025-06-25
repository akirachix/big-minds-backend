


# Create your models here.
from django.db import models
from order.models import Order
class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='api_payments')
    method = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now=True)
    def __str__(self):

from django.db import models
from users.models import Vendor

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    product_image = models.ImageField(upload_to='product_images/')
    unit = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class VendorProduct(models.Model):
    product_ddetails_id = models.AutoField(primary_key=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="api_vendor_products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_variants")
    price = models.FloatField()
    quantity = models.IntegerField()
    description = models.CharField(max_length=100)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.vendor.name} - {self.product.name}"

