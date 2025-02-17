from django.urls import path
from .views import CreateReviewView,ProductReviewListView,UserReviewListView,CreateReviewReplyView

urlpatterns = [
    path('create/', CreateReviewView.as_view(),name='create_review'),
    path('list/<int:product_id>/', ProductReviewListView.as_view(),name='list_reviews'),
    path('user-review/lists/', UserReviewListView.as_view(),name='user_reviews'),
    path('reply/', CreateReviewReplyView.as_view(),name='create_reply'),
]