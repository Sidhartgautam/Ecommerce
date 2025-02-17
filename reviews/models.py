from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    rating = models.PositiveIntegerField(null=True, blank=True)  # Rating out of 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.product.name}"

    def is_reply(self):
        return self.parent is not None
    
    def validate_rating(self):
        if self.parent is None: 
            if self.rating is None:
                raise ValueError("Rating is required for product reviews.")
            if self.rating < 1 or self.rating > 5:
                raise ValueError("Rating must be between 1 and 5.")

    def save(self, *args, **kwargs):
        self.validate_rating()  
        super().save(*args, **kwargs)