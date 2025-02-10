from django.contrib import admin
from .models import Category, Brand, Product, ProductAttribute, ProductImage

class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1  # Number of empty fields to display initially
    fields = ['name', 'value']
    verbose_name = "Product Attribute"
    verbose_name_plural = "Product Attributes"

# Inline for Product Images
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text']
    verbose_name = "Product Image"
    verbose_name_plural = "Product Images"

# Inline for Product Variants
class ProductVariantInline(admin.TabularInline):
    model = Product
    fk_name = 'parent_product'  # Use the parent_product relationship for variants
    extra = 1
    fields = ['name', 'format_name', 'price', 'stock_quantity', 'is_active']
    verbose_name = "Product Variant"
    verbose_name_plural = "Product Variants"

# Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'brand', 'price', 'stock_quantity', 'is_active']
    list_filter = ['category', 'brand', 'is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}  # Auto-generate slug from name
    inlines = [ProductAttributeInline, ProductImageInline, ProductVariantInline]

# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

# Brand Admin
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
