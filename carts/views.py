from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem, Product
from .serializers import CartSerializer, CartItemSerializer
from core.utils.response import PrepareResponse

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            cart, _ = Cart.objects.get_or_create(user=request.user)
            serializer = CartSerializer(cart)
            return PrepareResponse(
                success=True,
                message="Cart retrieved successfully.",
                data=serializer.data
            ).send(code=200)
        except Exception as e:
            return PrepareResponse(
                success=False,
                message="An error occurred while retrieving the cart.",
                errors={"detail": str(e)}
            ).send(code=500)

class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            product_id = request.data.get('product_id')
            quantity = request.data.get('quantity', 1)
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return PrepareResponse(
                    success=False,
                    message="Product not found.",
                    errors={"product": "Invalid product ID"}
                ).send(code=404)

            # Get or create the cart
            cart, _ = Cart.objects.get_or_create(user=request.user)

            # Add or update the cart item
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += int(quantity)
            else:
                cart_item.quantity = int(quantity)
            cart_item.save()

            return PrepareResponse(
                success=True,
                message="Product added to cart successfully.",
                data=CartItemSerializer(cart_item).data
            ).send(code=201)

        except Exception as e:
            return PrepareResponse(
                success=False,
                message="An error occurred while adding the product to the cart.",
                errors={"detail": str(e)}
            ).send(code=500)

class RemoveFromCartView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        try:
            product_id = kwargs.get('product_id')
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()

            if not cart_item:
                return PrepareResponse(
                    success=False,
                    message="Cart item not found.",
                    errors={"product": "No such item in the cart"}
                ).send(code=404)
            cart_item.delete()

            return PrepareResponse(
                success=True,
                message="Product removed from cart successfully."
            ).send(code=200)

        except Exception as e:
            return PrepareResponse(
                success=False,
                message="An error occurred while removing the product from the cart.",
                errors={"detail": str(e)}
            ).send(code=500)
