from orders.models import Order, OrderItem
from carts.models import Cart
from orders.serializers import OrderSerializer

def create_order(user, order_data):
    first_name = order_data.get('first_name')
    last_name = order_data.get('last_name')
    email = order_data.get('email')
    phone_number = order_data.get('phone_number')
    address = order_data.get('address')
    payment_method = order_data.get('payment_method', 'COD')
    if payment_method not in ['COD', 'Stripe']:
        return None, False, "Invalid payment method. Allowed values are 'COD' and 'Stripe'."
    cart = Cart.objects.filter(user=user).first()
    if not cart or not cart.items.exists():
        return None, False, "Cart is empty. Cannot place an order."
    order = Order.objects.create(
        user=user,
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=phone_number,
        address=address,
        payment_method=payment_method,
        payment_status='Unpaid' if payment_method == 'COD' else 'Paid'
    )
    for cart_item in cart.items.all():
        product = cart_item.product
        if product.stock_quantity < cart_item.quantity:
            return None, False, f"Insufficient stock for {product.name}."
        product.stock_quantity -= cart_item.quantity
        product.save()
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            price=cart_item.product.get_final_price()
        )
    order.calculate_total_price()

    cart.items.all().delete()

    return order, True, None
