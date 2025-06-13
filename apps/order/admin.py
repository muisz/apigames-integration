from django.contrib import admin

from apps.order.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_id', 'transaction_id', 'status', 'created_at')
    search_fields = ('transaction_id', 'order_id')
