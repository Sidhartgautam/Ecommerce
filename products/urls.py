from django.urls import path
from .views import ProductDetailView,ProductListView,RecommendedProductsView


urlpatterns = [
    path('product/lists/', ProductListView.as_view(),name='product_list'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/recommended/', RecommendedProductsView.as_view(), name='recommended_products'),
]