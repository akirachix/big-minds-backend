

# Register your models here.
from django.contrib import admin
from .models import Vendor, Buyer

admin.site.register(Vendor)
admin.site.register(Buyer)