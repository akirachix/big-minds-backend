from django.db import models
from users.models import Vendor

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    product_image = models.URLField(max_length=200)
    unit = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class VendorProduct(models.Model):
    product_ddetails_id = models.AutoField(primary_key=True)  
    vendor = models.ForeignKey( Vendor,on_delete=models.CASCADE, related_name='products_vendor_products',)
    product = models.ForeignKey( Product, on_delete=models.CASCADE, related_name='product_variants',)

    price = models.FloatField()
    quantity = models.IntegerField()
    description = models.TextField()
    added_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.vendor} - {self.product}"