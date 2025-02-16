from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = ['id', 'product', 'user', 'rating', 'comment', 'parent', 'replies', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def get_replies(self, obj):
        if obj.replies.exists():
            return ReviewSerializer(obj.replies.all(), many=True).data
        return []


class ReviewReplySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = ['id', 'product', 'user', 'comment', 'parent', 'created_at', 'updated_at']

    def validate(self, data):
        """Ensure parent is required for replies and rating is not included."""
        if 'parent' not in data or data['parent'] is None:
            raise serializers.ValidationError({"parent": "Parent review is required for replies."})

        if 'rating' in data:
            raise serializers.ValidationError({"rating": "Rating is not allowed for replies."})

        return data
