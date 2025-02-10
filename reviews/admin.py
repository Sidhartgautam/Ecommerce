from django.contrib import admin
from .models import Review

# Inline for Review Replies
class ReplyInline(admin.TabularInline):
    model = Review
    extra = 1  # Number of empty reply fields to display initially
    fields = ['user', 'rating', 'comment', 'created_at']
    readonly_fields = ['created_at']
    fk_name = 'parent'  # Use the parent relationship for replies
    verbose_name = "Reply"
    verbose_name_plural = "Replies"

# Review Admin
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'comment_preview', 'is_reply', 'created_at']
    list_filter = ['product', 'rating', 'created_at']
    search_fields = ['product__name', 'user__username', 'comment']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ReplyInline]

    def comment_preview(self, obj):
        return obj.comment[:50] + '...' if len(obj.comment) > 50 else obj.comment

    comment_preview.short_description = "Comment"
