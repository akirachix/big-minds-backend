from django.contrib import admin
from .models import Order, OrderedItem

class OrderedItemInline(admin.TabularInline):
    model = OrderedItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'buyer', 'vendor', 'total_price', 'status', 'order_date')
    search_fields = ('buyer__name', 'vendor__name', 'status')
    list_filter = ('status', 'order_date')
    inlines = [OrderedItemInline]

class OrderedItemAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'order', 'product', 'quantity', 'price_at_order')
    search_fields = ('order__order_id', 'product__name')

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderedItem, OrderedItemAdmin)