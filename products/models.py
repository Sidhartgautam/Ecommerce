from django.db import models
from core.utils.slugify import unique_slug_generator

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_generator(self, self.name)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name

# Brand Model
class Brand(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='brand_logos/', blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# Product Model
class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    discount_percentage= models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_variant = models.BooleanField(default=False)
    parent_product = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='variants')
    format_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def check_status(self):
        required_fields = [self.name, self.description, self.price, self.stock_quantity, self.category]
        if any(field is None or field == '' for field in required_fields):
            return "Incomplete (Product data missing)"
        if not self.attributes.exists():
            return "Incomplete (No attributes)"
        if not self.images.exists():
            return "Incomplete (No images)"
        if self.variants.exists():
            for variant in self.variants.all():
                if not (variant.name and variant.price and variant.stock_quantity):
                    return "Incomplete (Variant data missing)"

        return "Complete"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_generator(self, self.name)
        if self.parent_product:
            self.category = self.parent_product.category
            self.brand = self.parent_product.brand
        if self.parent_product:
            self.is_variant = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name if not self.is_variant else f"{self.parent_product.name} - {self.name}"

    def get_final_price(self):
        if self.discount_percentage > 0:
            discount_amount = (self.price * self.discount_percentage) / 100
            return self.price - discount_amount
        return self.price

class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')
    name = models.CharField(max_length=255,help_text="Name of the attribute like 'Ingredients', 'Material', 'Size")  # Example: 'Ingredients', 'Material', 'Size'
    value = models.TextField(help_text="Value of the attribute like 'Vitamin C', 'Wood', 'Large'")

    def __str__(self):
        return f"{self.name}: {self.value}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    alt_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.product.name}"
