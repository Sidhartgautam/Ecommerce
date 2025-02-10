# serializers.py
from rest_framework import serializers
from .models import NewsletterSubscriber

class NewsletterSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
