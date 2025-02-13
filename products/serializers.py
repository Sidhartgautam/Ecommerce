from rest_framework import serializers
from django.db import models
from .models import Category, Brand, Product, ProductAttribute, ProductImage

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug','image']

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'logo', 'description']

class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image','subcategories']

    def get_subcategories(self, obj):
        return CategorySerializer(obj.subcategories.all(), many=True).data

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image', 'alt_text']

class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ['name', 'value']

class ProductVariantOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'format_name', 'slug']

class ProductDetailSerializer(serializers.ModelSerializer):
    final_price = serializers.SerializerMethodField()
    discount_label = serializers.SerializerMethodField()
    attributes = ProductAttributeSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    format_options = serializers.SerializerMethodField()
    category=serializers.CharField(source='category.name')
    brand=serializers.CharField(source='brand.name')

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug','category','brand','description','stock_quantity', 'price', 'final_price', 'discount_label',
            'attributes', 'images', 'format_options'
        ]

    def get_final_price(self, obj):
        return obj.get_final_price()

    def get_discount_label(self, obj):
        if obj.discount_percentage > 0:
            return f"{obj.discount_percentage}% OFF"
        return None

    def get_format_options(self, obj):
        if obj.is_variant and obj.parent_product:
            parent_product = obj.parent_product
            sibling_variants = parent_product.variants.exclude(id=obj.id)
            products = [obj, parent_product] + list(sibling_variants)
        else:
            variants = obj.variants.all()
            products = [obj] + list(variants)
        return ProductVariantOptionSerializer(products, many=True).data
class ProductListSerializer(serializers.ModelSerializer):
    final_price = serializers.SerializerMethodField()
    discount_label = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'price', 'final_price', 'discount_label',
            'rating', 'reviews_count', 'image'
        ]

    def get_final_price(self, obj):
        return obj.get_final_price()

    def get_discount_label(self, obj):
        if obj.discount_percentage > 0:
            return f"{obj.discount_percentage}% OFF"
        return None

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            return round(reviews.aggregate(models.Avg('rating'))['rating__avg'], 1)
        return None

    def get_reviews_count(self, obj):
        return obj.reviews.count()

    def get_image(self, obj):
        image = obj.images.first()
        if image:
            return image.image.url
        return None
    
class PopularProductSerializer(serializers.ModelSerializer):
    final_price = serializers.SerializerMethodField()
    discount_label = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    orders_count = serializers.IntegerField(read_only=True)
    rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'price', 'final_price', 'discount_label',
            'orders_count', 'image', 'rating', 'reviews_count'
        ]

    def get_final_price(self, obj):
        return obj.get_final_price()

    def get_discount_label(self, obj):
        if obj.discount_percentage > 0:
            return f"{obj.discount_percentage}% OFF"
        return None

    def get_image(self, obj):
        image = obj.images.first()
        return image.image.url if image else None
    
    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            return round(reviews.aggregate(models.Avg('rating'))['rating__avg'], 1)
        return None

    def get_reviews_count(self, obj):
        return obj.reviews.count()