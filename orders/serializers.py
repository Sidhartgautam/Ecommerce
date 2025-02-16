from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    total_price = serializers.SerializerMethodField()
    product_image = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name','product_image', 'price', 'quantity', 'total_price']

    def get_total_price(self, obj):        
        return obj.total_price()
    
    def get_product_image(self, obj):
        first_image = obj.product.images.first()
        if first_image:
            return first_image.image.url
        return None

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_id', 'first_name','last_name', 'email', 'phone_number', 'address',
            'status', 'payment_method', 'payment_status', 'total_price', 'items',
            'created_at', 'updated_at'
        ]
