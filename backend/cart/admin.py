from django.contrib import admin


# Register your models here.

from django.contrib import admin

from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
   model = CartItem
   extra = 1


class CartAdmin(admin.ModelAdmin):
   list_display = ('cart_id', 'customer', 'added_at')
   search_fields = ('customer__name',)
   inlines = [CartItemInline]


class CartItemAdmin(admin.ModelAdmin):
   list_display = ('cart', 'product', 'quantity', 'added_at')
   search_fields = ('cart__customer__name', 'product__name')


admin.site.register(Cart, CartAdmin)

admin.site.register(CartItem, CartItemAdmin)


admin.site.register(CartItem, CartItemAdmin)

