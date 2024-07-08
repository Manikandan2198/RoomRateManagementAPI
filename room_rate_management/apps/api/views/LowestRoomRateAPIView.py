from datetime import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.models import Discount, DiscountRoomRate, OverriddenRoomRate, RoomRate
from apps.api.serializers import LowestRoomRateListSerializer, RoomRateSerializer
from apps.api.services.LowestRoomRateService import get_lowest_room_rates

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Create your views here.

class LowestRoomRateAPI(APIView):
    
    @swagger_auto_schema(
        operation_description="Get the lowest room rates in a specific date range",
        manual_parameters=[
            openapi.Parameter(
                name="start_date",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Stay date",
                required=True,
                example="2024-07-10",
            ),
            openapi.Parameter(
                name="end_date",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Stay date",
                required=True,
                example="2024-07-12",
            )
        ],
        responses={
            200: openapi.Response(
                description="Successful operation",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'date': openapi.Schema(type=openapi.FORMAT_DATE, format=openapi.FORMAT_DATE, example='2024-07-10'),
                            'lowest_rate': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, example=120.5)
                        }
                    )
                ),
            ),
            400: "Invalid input",
            404: "Room rate not found",
            500: "Internal server error",
        }
    )
    def get(self, request, room_id=None):
        if room_id is None:
            return Response({"error_message":"Room id not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        start_date=request.query_params.get('start_date', None)
        end_date=request.query_params.get('end_date', None)
        if start_date is None or end_date is None:
            return Response({"error_message":"Date range not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            room_rate = RoomRate.objects.get(room_id = room_id)
        except RoomRate.DoesNotExist:
            return Response({"error_message":"Room rate not found"}, status=status.HTTP_404_NOT_FOUND)
        
        lowest_room_rates = get_lowest_room_rates(room_rate,start_date,end_date)   
        serializer = LowestRoomRateListSerializer(lowest_room_rates,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


            




        