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
   product_details_id = models.AutoField(primary_key=True)
   vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="vendor_products")
   product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_variants")
   price = models.FloatField()
   quantity = models.IntegerField()
   description = models.CharField(max_length=100)
   added_on = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)


   def __str__(self):
       return f"{self.vendor.name} - {self.product.name}"