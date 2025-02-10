from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'product', 'user', 'rating', 'comment', 'parent', 'replies', 'created_at', 'updated_at']

    def get_replies(self, obj):
        if obj.replies.exists():
            return ReviewSerializer(obj.replies.all(), many=True).data
        return []
