from django.urls import path
from .views import (ProductDetailView,
                    ProductListView,
                    RecommendedProductsView,
                    CategoryListView,
                    ProductListByCategoryView,
                    PopularProductsView,
                    NavbarCategoryListView,
                    RecentlyAddedProductsView
)


urlpatterns = [
    path('category/navbar/lists/', NavbarCategoryListView.as_view(),name='navbar_category_list'),
    path('category/lists/', CategoryListView.as_view(),name='category_list'),
    path('productbycategory/<slug:category_slug>/', ProductListByCategoryView.as_view(), name='product_list_by_category'),
    path('product/lists/', ProductListView.as_view(),name='product_list'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/recommendation/lists/', RecommendedProductsView.as_view(), name='recommended_products'),
    path('products/popular/lists/', PopularProductsView.as_view(), name='popular_products'),
    path('products/recent/lists/', RecentlyAddedProductsView.as_view(), name='recently_added_products'),
]
