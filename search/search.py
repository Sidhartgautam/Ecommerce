from django.db.models import Q, Avg, F, Value
from django.db.models.functions import Coalesce
from django.db.models import DecimalField
from products.models import Product, Category, Brand
from rest_framework.pagination import PageNumberPagination

def search_products(query=None, price_min=None, price_max=None, sort_price=None, discount_percentage=None, ratings=None, category=None, brand=None):
    try:
        price_min = float(price_min) if price_min else None
        price_max = float(price_max) if price_max else None
        ratings = float(ratings) if ratings else None
    except ValueError:
        price_min = price_max = ratings = None

    # Initialize querysets
    product_results = Product.objects.none()
    category_results = Category.objects.none()
    brand_results = Brand.objects.none()

    # Check which parameters are being used
    has_product_params = any([query, price_min, price_max, sort_price, discount_percentage, ratings, category, brand])
    has_category_params = category is not None
    has_brand_params = brand is not None

    if not any([has_product_params, has_category_params, has_brand_params]):
        product_results = Product.objects.all()[:10]

    # Category search
    if has_category_params:
        category_results = Category.objects.filter(name__icontains=category)

    # Brand search
    if has_brand_params:
        brand_results = Brand.objects.filter(name__icontains=brand)

    # Product search with filters
    if has_product_params:
        product_filters = Q()

        if query:
            product_filters |= Q(name__icontains=query) | Q(description__icontains=query)
        
        if category:
            product_filters &= Q(category__name__icontains=category)
        
        if brand:
            product_filters &= Q(brand__name__icontains=brand)

        # Annotate product ratings
        product_results = Product.objects.annotate(
            average_rating=Avg('reviews__rating'),
            final_price=Coalesce(
                F('price') * (1 - F('discount_percentage') / Value(100.0)),
                F('price'),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        )

        # Apply filters
        if ratings is not None:
            product_results = product_results.filter(average_rating__gte=ratings)
        if price_min is not None:
            product_results = product_results.filter(final_price__gte=price_min)
        if price_max is not None:
            product_results = product_results.filter(final_price__lte=price_max)

        # Sorting
        if sort_price == 'low_to_high':
            product_results = product_results.order_by('final_price')
        elif sort_price == 'high_to_low':
            product_results = product_results.order_by('-final_price')

    # Prepare response
    response = {}

    if category_results.exists():
        response['categories'] = category_results
    if brand_results.exists():
        response['brands'] = brand_results
    if product_results.exists():
        response['products'] = product_results

    return response if response else None
