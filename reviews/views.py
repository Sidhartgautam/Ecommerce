from rest_framework import generics
from .models import Review
from .serializers import ReviewSerializer
from core.utils.response import PrepareResponse
from django.http import Http404
from rest_framework.permissions import IsAuthenticated

class ProductReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        return Review.objects.filter(product_id=product_id, parent__isnull=True).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return PrepareResponse(
                success=True,
                message="List of reviews",
                data=serializer.data
            ).send(code=200)

        except Exception as e:
            return PrepareResponse(
                success=False,
                message="An error occurred while fetching reviews.",
                errors={"detail": str(e)}
            ).send(code=500)
class CreateReviewView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return PrepareResponse(
                success=True,
                message="Review created successfully",
                data=serializer.data
            ).send(code=201)

        except Exception as e:
            return PrepareResponse(
                success=False,
                message="An error occurred while creating the review.",
                errors={"detail": str(e)}
            ).send(code=500)
        
class UserReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return PrepareResponse(
                success=True,
                message="List of user reviews",
                data=serializer.data
            ).send(code=200)

        except Exception as e:
            return PrepareResponse(
                success=False,
                message="An error occurred while fetching user reviews.",
                errors={"detail": str(e)}
            ).send(code=500)

