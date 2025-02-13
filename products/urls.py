from django.urls import path
from .views import ProductDetailView,ProductListView,RecommendedProductsView,CategoryListView,ProductListByCategoryView


urlpatterns = [
    path('category/lists/', CategoryListView.as_view(),name='category_list'),
    path('productbycategory/<slug:category_slug>/', ProductListByCategoryView.as_view(), name='product_list_by_category'),
    path('product/lists/', ProductListView.as_view(),name='product_list'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/recommended/', RecommendedProductsView.as_view(), name='recommended_products'),
]