from django.contrib import admin
from .models import Order, OrderItem

# Inline for Order Items
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Number of empty fields to display initially
    fields = ['product', 'quantity', 'price']
    readonly_fields = ['total_price']
    can_delete = True
    verbose_name = "Order Item"
    verbose_name_plural = "Order Items"

    def total_price(self, obj):
        return obj.total_price()

    total_price.short_description = "Total Price (Item)"


# Order Admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'first_name', 'email', 'status', 'payment_method', 'payment_status', 'total_price', 'created_at']
    list_filter = ['status', 'payment_method', 'payment_status', 'created_at']
    search_fields = ['order_id', 'first_name', 'email', 'phone_number']
    date_hierarchy = 'created_at'
    readonly_fields = ['order_id', 'total_price', 'created_at', 'updated_at']
    inlines = [OrderItemInline]

    # Custom method to calculate total price dynamically
    def calculate_total_price(self, obj):
        return f"{obj.total_price} USD"

    calculate_total_price.short_description = "Total Price"


# OrderItem Admin (if needed separately)
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price', 'total_price']
    search_fields = ['order__order_id', 'product__name']
    list_filter = ['order__status']
