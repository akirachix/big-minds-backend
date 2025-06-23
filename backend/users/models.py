from django.db import models

class Vendor(models.Model):
    vendor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    password_hash = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='vendors/', blank=True, null=True)
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    shop_name = models.CharField(max_length=100)
    till_number = models.IntegerField(unique=True)

    def __str__(self):
        return self.name

class Buyer(models.Model):
    buyer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    password_hash = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='buyers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name          
    
                                                                                  