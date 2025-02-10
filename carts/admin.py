from django.contrib import admin
from .models import Cart, CartItem

# Inline for Cart Items
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1  # Number of empty fields to display initially
    fields = ['product', 'quantity', 'total_price']
    readonly_fields = ['total_price']
    verbose_name = "Cart Item"
    verbose_name_plural = "Cart Items"

    # Custom method to calculate total price for the inline display
    def total_price(self, obj):
        return obj.total_price()

    total_price.short_description = "Total Price (Item)"


# Cart Admin
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'item_count', 'total_cart_price', 'created_at']
    search_fields = ['user__username']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']
    inlines = [CartItemInline]

    # Custom method to display the total price of all items in the cart
    def total_cart_price(self, obj):
        return f"{obj.total_price()} USD"

    total_cart_price.short_description = "Total Cart Price"

    # Custom method to display the number of items in the cart
    def item_count(self, obj):
        return obj.items.count()

    item_count.short_description = "Number of Items"


# CartItem Admin (if needed separately)
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'total_price']
    search_fields = ['cart__user__username', 'product__name']
    list_filter = ['cart__user']
    readonly_fields = ['total_price']

    def total_price(self, obj):
        return obj.total_price()

    total_price.short_description = "Total Price (Item)"
