from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = (
        'user_id', 'name', 'phone_number', 'type', 
        'location', 'shop_name', 'till_number', 
        'created_at', 'last_login'
    )
    list_filter = ('type', 'created_at', 'last_login')
    search_fields = ('name', 'phone_number', 'shop_name', 'location')
    readonly_fields = ('created_at', 'last_login')

admin.site.register(User, UserAdmin)