from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Payment
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id',  'method', 'status', 'amount', 'created_at')
    list_filter = ('status', 'method', 'created_at')
    
admin.site.register(Payment, PaymentAdmin)