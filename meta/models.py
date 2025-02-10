from django.db import models

# Create your models here.
class CompanyDetails(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    facebook = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    youtube = models.URLField(null=True, blank=True)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)

class Policies(models.Model):
    terms_and_conditions = models.TextField()
    privacy_policy = models.TextField()
    return_policy = models.TextField()
    refund_policy = models.TextField()
    shipping_policy = models.TextField()

    def __str__(self):
        return self.terms_and_conditions
