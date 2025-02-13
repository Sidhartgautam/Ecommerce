from django.urls import path
from .views import CreateOrderView, CancelOrderView, UserOrdersListView

urlpatterns = [
    path('create/', CreateOrderView.as_view(), name='create_order'),
    path('cancel/<str:order_id>/', CancelOrderView.as_view(), name='cancel_order'),
    path('user/order-lists/', UserOrdersListView.as_view(), name='user_orders'),

]