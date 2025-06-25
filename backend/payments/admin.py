from django.contrib import admin
from .models import Payment
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'order', 'method', 'status', 'amount', 'created_at')
    list_filter = ('status', 'method', 'created_at')
    search_fields = ('order__order_id',)
    
admin.site.register(Payment, PaymentAdmin)