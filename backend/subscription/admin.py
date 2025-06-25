from django.contrib import admin
from .models import SubscriptionBox, ScheduledItem




class ScheduledItemInline(admin.TabularInline):
  model = ScheduledItem
  extra = 1




class SubscriptionBoxAdmin(admin.ModelAdmin):
  list_display = ('schedule_id', 'name', 'buyer', 'vendor', 'frequency', 'price', 'start_date', 'status')
  search_fields = ('name', 'buyer__name', 'vendor__name', 'status')
  list_filter = ('frequency', 'status', 'start_date')
  inlines = [ScheduledItemInline]


admin.site.register(SubscriptionBox, SubscriptionBoxAdmin)
admin.site.register(ScheduledItem)
