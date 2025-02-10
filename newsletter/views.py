# views.py
from rest_framework.views import APIView
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from .models import NewsletterSubscriber
from .serializers import NewsletterSubscriptionSerializer
from core.utils.response import PrepareResponse

class NewsletterSubscriptionView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = NewsletterSubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.data['email']

            # Send confirmation email
            self.send_subscription_email(email)

            return PrepareResponse(
                success=True,
                message="Thank you for subscribing to our newsletter!",
                data=serializer.data
            ).send(code=201)
        else:
            return PrepareResponse(
                success=False,
                message="Subscription failed. Please provide a valid email.",
                errors=serializer.errors
            ).send(code=400)

    def send_subscription_email(self, email):
        subject = "Newsletter Subscription Confirmation"
        message = (
            "Thank you for subscribing to our newsletter!\n\n"
            "You will now receive updates on our latest products, offers, and news."
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
