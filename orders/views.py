from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from core.utils.order import create_order
from .serializers import OrderSerializer
from core.utils.response import PrepareResponse

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
