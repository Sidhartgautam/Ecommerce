from .serializers import (ProductListSerializer,
                          ProductDetailSerializer,
                          CategoryListSerializer,
                          CategorySerializer,
                          PopularProductSerializer
)
from django.db.models import Count
from rest_framework.views import APIView
from .models import Product,Category
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.generics import ListAPIView
from core.utils.pagination import CustomPageNumberPagination
from core.utils.response import PrepareResponse
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound

class CategoryListView(ListAPIView):
    queryset = Category.objects.filter(parent__isnull=True)  
    serializer_class = CategoryListSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)

            return PrepareResponse(
                success=True,
                message="Category list retrieved successfully.",
                data=serializer.data
            ).send(code=200)

        except Exception as e:
            return PrepareResponse(
                success=False,
                message="An error occurred while retrieving categories.",
                errors={"detail": str(e)}
            ).send(code=500)
        
class NavbarCategoryListView(ListAPIView):
    queryset = Category.objects.filter(parent__isnull=True) 
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)

            return PrepareResponse(
                success=True,
                message="Navbar Category list retrieved successfully.",
                data=serializer.data
            ).send(code=200)

        except Exception as e:
            return PrepareResponse(
                success=False,
                message="An error occurred while retrieving categories.",
                errors={"detail": str(e)}
            ).send(code=500)

class ProductListByCategoryView(ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        category = get_object_or_404(Category, slug=category_slug)
        return Product.objects.filter(category=category, is_active=True)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)

            return PrepareResponse(
                success=True,
                message="Product list retrieved successfully.",
                data=serializer.data
            ).send(code=200)

        except Exception as e:
            return PrepareResponse(
                success=False,
                message="An error occurred while retrieving products.",
                errors={"detail": str(e)}
            ).send(code=500)

class ProductListView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Product.objects.filter(is_active=True)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                paginated_response = self.get_paginated_response(serializer.data)
                response_data = {
                    "products": paginated_response["results"],
                    "meta": {
                        "page_number": paginated_response["page_number"],
                        "total_pages": paginated_response["total_pages"],
                        "total_items": paginated_response["count"],
                        "links": paginated_response["links"],
                    },
                }
                return PrepareResponse(
                    success=True,
                    message="List of products",
                    data=response_data
                ).send(code=200)
            
            serializer = self.get_serializer(queryset, many=True)
            return PrepareResponse(
                success=True,
                message="List of products",
                data=serializer.data
            ).send(code=200)

        except Exception as e:
            return PrepareResponse(
                success=False,
                message="An error occurred while fetching the product list.",
                errors={"detail": str(e)}
            ).send(code=500)
        
class ProductDetailView(generics.RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    permission_classes=[AllowAny]
    lookup_field = 'slug'

    def get_queryset(self):
        return Product.objects.filter(is_active=True)

    def retrieve(self, request, *args, **kwargs):
        try:
            product = self.get_object()
            serializer = self.get_serializer(product)
            return PrepareResponse(
                success=True,
                message="Product details retrieved successfully.",
                data=serializer.data
            ).send(code=200)

        except Product.DoesNotExist:
            return PrepareResponse(
                success=False,
                message="Product not found.",
                errors={"slug": "No product found with the provided slug."}
            ).send(code=404)
        
class RecommendedProductsView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes=[AllowAny]

    def get_queryset(self):
        current_product_slug = self.request.query_params.get('product_slug')

        if not current_product_slug:
            raise NotFound(detail="Product slug is required.", code=400)
        current_product = Product.objects.filter(slug__iexact=current_product_slug).first()
        if not current_product:
            raise NotFound(detail=f"No product found with slug '{current_product_slug}'.", code=404)
        recommended_products = Product.objects.filter(is_active=True).exclude(id=current_product.id)
        category_products = recommended_products.filter(category=current_product.category)
        brand_products = recommended_products.filter(brand=current_product.brand)
        recommended_products = (category_products | brand_products).distinct()[:10]
        return recommended_products

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()

            serializer = self.get_serializer(queryset, many=True)
            return PrepareResponse(
                success=True,
                message="Recommended products retrieved successfully.",
                data=serializer.data
            ).send(code=200)

        except Exception as e:
            return PrepareResponse(
                success=False,
                message="An error occurred while fetching recommended products.",
                errors={"detail": str(e)}
            ).send(code=500)
        
class PopularProductsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            popular_products = Product.objects.annotate(
                orders_count=Count('orderitem')
            ).order_by('-orders_count')[:10]
            serializer = PopularProductSerializer(popular_products, many=True, context={'request': request})
            if not popular_products.exists():
                return PrepareResponse(
                    success=True,
                    message="No popular products found.",
                    data=[]
                ).send(code=200)

            return PrepareResponse(
                success=True,
                message="Popular products retrieved successfully.",
                data=serializer.data
            ).send(code=200)

        except Exception as e:
            return PrepareResponse(
                success=False,
                message="An error occurred while retrieving popular products.",
                errors={"detail": str(e)}
            ).send(code=500)
        
class RecentlyAddedProductsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            recently_added_products = Product.objects.filter(is_active=True).order_by('-created_at')[:10]  

            serializer = ProductListSerializer(recently_added_products, many=True, context={'request': request})          
            if not recently_added_products.exists():
                return PrepareResponse(
                    success=True,
                    message="No recently added products found.",
                    data=[]
                ).send(code=200)

            return PrepareResponse(
                success=True,
                message="Recently added products retrieved successfully.",
                data=serializer.data
            ).send(code=200)

        except Exception as e:
            return PrepareResponse(
                success=False,
                message="An error occurred while retrieving recently added products.",
                errors={"detail": str(e)}
            ).send(code=500)
    
    
