from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.models import Discount, DiscountRoomRate, RoomRate
from apps.api.serializers import RoomRateSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Create your views here.

class DiscountRoomRateAPI(APIView):
    
    @swagger_auto_schema(
        operation_description="Assign discounts to room rates",
        request_body=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'room_id': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                    'discounts':openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items = openapi.Schema(type=openapi.TYPE_NUMBER, example=1)
                    )
                },
            ),
        ),
        responses={
            201: "Discounts are successfully assigned to RoomRates",
            400: "Invalid input",
            404: "Room rate or discount not found",
            500: "Internal server error",
        }
    )
    def post(self, request):
        for item in request.data:
            room_id = item.get('room_id')
            discount_ids = item.get('discounts')

            try:
                room_rate = RoomRate.objects.get(room_id=room_id)
            except RoomRate.DoesNotExist:
                return Response({'error': f'Room "{room_rate.room_name}" does not exist'}, status=status.HTTP_404_NOT_FOUND)
            
            for discount_id in discount_ids:
                try:
                    discount = Discount.objects.get(discount_id=discount_id)
                except Discount.DoesNotExist:
                    return Response({'error': f'Discount "{discount.discount_name}" does not exist'}, status=status.HTTP_404_NOT_FOUND)

                room_rate_discount, created = DiscountRoomRate.objects.get_or_create(room_rate=room_rate, discount=discount)
                if not created:
                    return Response({'error': f'The mapping of Room "{room_rate.room_name}" and Discount "{discount.discount_name}" already exists'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Discounts are successfully assigned to RoomRates'}, status=status.HTTP_201_CREATED)
    

        