from rest_framework import serializers
from django.db import models
from .models import Category, Brand, Product, ProductAttribute, ProductImage

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

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price', 'final_price', 'discount_label',
            'attributes', 'images', 'format_options'
        ]

    def get_final_price(self, obj):
        return obj.get_final_price()

    def get_discount_label(self, obj):
        if obj.discount_percentage > 0:
            return f"{obj.discount_percentage}% OFF"
        return None

    def get_format_options(self, obj):
        if not obj.is_variant:
            # Fetch all variants linked to this product
            variants = obj.variants.all()
            return ProductVariantOptionSerializer(variants, many=True).data
        elif obj.parent_product:
            # Fetch all siblings (variants) under the same parent product
            return ProductVariantOptionSerializer(obj.parent_product.variants.all(), many=True).data
        return []
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