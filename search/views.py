from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from core.utils.response import PrepareResponse
from .search import search_products
from products.serializers import ProductListSerializer, CategoryListSerializer,BrandSerializer
from core.utils.pagination import CustomPageNumberPagination

class ProductSearchView(APIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPageNumberPagination

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('query', None)
        price_min = request.query_params.get('price_min', None)
        price_max = request.query_params.get('price_max', None)
        sort_price = request.query_params.get('sort_price', None)
        discount_percentage = request.query_params.get('discount_percentage', None)
        ratings = request.query_params.get('ratings', None)
        category = request.query_params.get('category', None)
        brand = request.query_params.get('brand', None)

        # Fetch search results
        results = search_products(
            query=query,
            price_min=price_min,
            price_max=price_max,
            sort_price=sort_price,
            discount_percentage=discount_percentage,
            ratings=ratings,
            category=category,
            brand=brand
        )

        if not results or not any(results.values()):
            return PrepareResponse(success=False, message="No results found").send(404)

        paginated_response = {}

        # Paginate products
        if results.get('products'):
            paginator = self.pagination_class()
            paginated_products = paginator.paginate_queryset(results['products'], request)
            product_serializer = ProductListSerializer(paginated_products, many=True, context={'request': request})
            paginated_response['products'] = paginator.get_paginated_response(product_serializer.data)

        # Paginate categories
        if results.get('categories'):
            paginator = self.pagination_class()
            paginated_categories = paginator.paginate_queryset(results['categories'], request)
            category_serializer = CategoryListSerializer(paginated_categories, many=True)
            paginated_response['categories'] = paginator.get_paginated_response(category_serializer.data)

        # Paginate brands
        if results.get('brands'):
            paginator = self.pagination_class()
            paginated_brands = paginator.paginate_queryset(results['brands'], request)
            brand_serializer = BrandSerializer(paginated_brands, many=True, context={'request': request})
            paginated_response['brands'] = paginator.get_paginated_response(brand_serializer.data)

        return PrepareResponse(success=True, data=paginated_response, message="Search results retrieved successfully").send(200)
