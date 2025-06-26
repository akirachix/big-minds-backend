from django.db import models

USER_TYPE_CHOICES = [
    ('vendor', 'Vendor (Mama Mboga)'),
    ('customer', 'Customer (Buyer)'),
]

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    password_hash = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='users/', blank=True, null=True)
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    
    shop_name = models.CharField(max_length=100, blank=True, null=True)
    till_number = models.IntegerField(blank=True, null=True, unique=True)
    
  
    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"