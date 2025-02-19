from django.core.mail import send_mail
from django.conf import settings

OWNER_EMAIL = "owner@yourshop.com"  # Replace with the owner's email

def send_order_email(order):
    """Send order confirmation email to both the customer and the owner."""
    
    subject = f"Order Confirmation - {order.order_id}"
    message = f"""
    Hi {order.first_name},

    Thank you for your order #{order.order_id}!
    Your order is currently being processed. Here are the details:

    - Name: {order.first_name} {order.last_name}
    - Email: {order.email}
    - Phone: {order.phone_number}
    - Address: {order.address}
    - Payment Method: {order.payment_method}
    - Total Price: ${order.total_price}

    We will update you when your order is shipped.

    Thanks,
    YourShop Team
    """
    recipients = [order.email, OWNER_EMAIL]

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipients, 
        fail_silently=False,
    )

def send_cancel_order_email(order):
    """Send cancellation email to both the customer and the owner."""
    
    subject = f"Order Canceled - {order.order_id}"
    message = f"""
    Hi {order.first_name},

    Your order #{order.order_id} has been canceled.

    If you have any questions, feel free to contact our support team.

    Thanks,
    YourShop Team
    """

    # List of recipients (Customer + Owner)
    recipients = [order.email, OWNER_EMAIL]

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipients,
        fail_silently=False,
    )
