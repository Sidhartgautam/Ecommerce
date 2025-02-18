from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from core.utils.order import create_order
from orders.models import Order
from .serializers import OrderSerializer
from core.utils.response import PrepareResponse
from core.utils.email import send_cancel_order_email

class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            order, success, error_message = create_order(request.user, request.data)

            if not success:
                return PrepareResponse(
                    success=False,
                    message=error_message,
                    errors={"order": error_message}
                ).send(code=400)

            return PrepareResponse(
                success=True,
                message="Order placed successfully.",
                data=OrderSerializer(order).data
            ).send(code=201)

        except Exception as e:
            return PrepareResponse(
                success=False,
                message="An error occurred while placing the order.",
                errors={"detail": str(e)}
            ).send(code=500)

class UserOrdersListView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)

            return PrepareResponse(
                success=True,
                message="User orders retrieved successfully.",
                data=serializer.data
            ).send(code=200)

        except Exception as e:
            return PrepareResponse(
                success=False,
                message="An error occurred while retrieving orders.",
                errors={"detail": str(e)}
            ).send(code=500)
        

class CancelOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id, *args, **kwargs):
        try:
            order = Order.objects.filter(order_id=order_id, user=request.user).first()

            if not order:
                return PrepareResponse(
                    success=False,
                    message="Order not found.",
                    errors={"order": "Order not found."}
                ).send(code=404)

            if order.status in ["Canceled", "Delivered"]:
                return PrepareResponse(
                    success=False,
                    message="Order cannot be canceled.",
                    errors={"order": "Order has already been delivered or canceled."}
                ).send(code=400)

            order.status = "Canceled"
            order.save()
            send_cancel_order_email(order)

            return PrepareResponse(
                success=True,
                message="Order has been successfully canceled.",
                data=OrderSerializer(order).data
            ).send(code=200)

        except Exception as e:
            return PrepareResponse(
                success=False,
                message="An error occurred while canceling the order.",
                errors={"detail": str(e)}
            ).send(code=500)

