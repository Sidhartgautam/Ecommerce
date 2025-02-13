from django.urls import path
from .views import CreateReviewView,ProductReviewListView,UserReviewListView

urlpatterns = [
    path('create/', CreateReviewView.as_view(),name='create_review'),
    path('list/', ProductReviewListView.as_view(),name='list_reviews'),
    path('user-review/lists/', UserReviewListView.as_view(),name='user_reviews'),
]