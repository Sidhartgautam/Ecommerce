from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Brand, Product, ProductAttribute, ProductImage

class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1  # Number of empty fields to display initially
    fields = ['name', 'value']
    verbose_name = "Product Attribute"
    verbose_name_plural = "Product Attributes"
    classes=['wide']

# Inline for Product Images
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text']
    verbose_name = "Product Image"
    verbose_name_plural = "Product Images"
    classes=['wide']

#Variant Filter
class VariantFilter(admin.SimpleListFilter):
    title = 'Product Type'
    parameter_name = 'product_type'

    def lookups(self, request, model_admin):
        return [
            ('parent', 'Parent Products'),
            ('variant', 'Variants'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'parent':
            return queryset.filter(parent_product__isnull=True) 
        if self.value() == 'variant':
            return queryset.filter(parent_product__isnull=False) 
        return queryset

# Inline for Product Variants
class ProductVariantInline(admin.StackedInline):
    model = Product
    fk_name = 'parent_product'
    extra = 1
    fields = ['name', 'format_name', 'price','description','discount_percentage', 'stock_quantity', 'is_active']
    verbose_name = "Product Variant"
    verbose_name_plural = "Product Variants"
    show_change_link = True
    inlines = [ProductImageInline]
    classes=['wide']

########ProductStatusFilter
class ProductStatusFilter(admin.SimpleListFilter):
    title = 'Product Status'
    parameter_name = 'product_status'

    def lookups(self, request, model_admin):
        """Define filter options."""
        return [
            ('complete', 'Complete'),
            ('incomplete', 'Incomplete'),
        ]

    def queryset(self, request, queryset):
        """Apply the filter based on product status."""
        if self.value() == 'complete':
            # Collect IDs of products that are complete
            complete_ids = [product.id for product in queryset if product.check_status() == "Complete"]
            return queryset.filter(id__in=complete_ids)

        elif self.value() == 'incomplete':
            incomplete_ids = [product.id for product in queryset if "Incomplete" in product.check_status()]
            return queryset.filter(id__in=incomplete_ids)

        return queryset
# Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'brand', 'price', 'stock_quantity', 'is_active', 'status']
    list_filter = ['category', 'brand', 'is_active', VariantFilter, ProductStatusFilter]
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductAttributeInline, ProductImageInline, ProductVariantInline]

    def status(self, obj):
        status = obj.check_status()
        if "Incomplete" in status:
            return format_html('<span style="color: red; font-weight: bold;">{}</span>', status)
        return format_html('<span style="color: green; font-weight: bold;">{}</span>', status)

    status.short_description = "Product Status"

    def is_variant_status(self, obj):
        return "Variant" if obj.parent_product else "Parent Product"

    is_variant_status.short_description = "Product Type"
    is_variant_status.admin_order_field = 'parent_product'




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


