from datetime import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.models import OverriddenRoomRate, RoomRate
from apps.api.serializers import OverriddenRoomRateSerializer, OverriddenRoomRateUpdateSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Create your views here.

class OverriddenRoomRatePostAPI(APIView):
    @swagger_auto_schema(
        operation_description="Create a new overridden room rate",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'room_rate': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                'overridden_rate': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, example=120.5),
                'stay_date': openapi.Schema(type=openapi.FORMAT_DATE, format=openapi.FORMAT_FLOAT, example='2024-07-10')
            },
        ),
        responses={
            201: openapi.Response(
                description="Successful operation",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'room_rate': openapi.Schema(
                            type=openapi.TYPE_OBJECT, 
                            properties={
                                'room_id': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                                'room_name':openapi.Schema(type=openapi.TYPE_STRING, example="deluxe room"),
                                'default_rate': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, example=120.5)
                            }
                        ),
                        'overridden_rate':openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, example=120.5),
                        'stay_date': openapi.Schema(type=openapi.FORMAT_DATE, format=openapi.FORMAT_DATE, example='2024-07-10')
                    },
                ),
            ),
            400: "Invalid input",
            500: "Internal server error",
        }
    )
    def post(self, request):
        serializer = OverriddenRoomRateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OverriddenRoomRateDetailAPI(APIView):

    @swagger_auto_schema(
        operation_description="Get all overridden room rates of a specific room id",
        responses={
            200: openapi.Response(
                description="Successful operation",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'room_rate': openapi.Schema(
                            type=openapi.TYPE_OBJECT, 
                            properties={
                                'room_id': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                                'room_name':openapi.Schema(type=openapi.TYPE_STRING, example="deluxe room"),
                                'default_rate': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, example=120.5)
                            }
                        ),
                        'overridden_rate':openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, example=120.5),
                        'stay_date': openapi.Schema(type=openapi.FORMAT_DATE, format=openapi.FORMAT_FLOAT, example='2024-07-10')
                    },
                ),
            ),
            400: "Invalid input",
            404: "Room/Overridden rate not found",
            500: "Internal server error",
        }
    )
    def get(self, request,room_id=None): 
        if room_id is None:
            return Response({"error_message":"Room Id not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            room_rate = RoomRate.objects.get(room_id = room_id)
        except RoomRate.DoesNotExist:
            return Response({"error_message":"Room rate not found"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            overridden_room_rate = OverriddenRoomRate.objects.filter(room_rate = room_rate)
        except OverriddenRoomRate.DoesNotExist:
            return Response({"error_message":"Overridden room rate not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = OverriddenRoomRateSerializer(overridden_room_rate,many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Update an existing overridden room rate by room id and stay date",
        manual_parameters=[
            openapi.Parameter(
                name="stay_date",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Stay date",
                required=True,
                example="2024-07-10",
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'overridden_rate': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, example=120.5)
            },
        ),
        responses={
            201: openapi.Response(
                description="Successful operation",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'room_rate': openapi.Schema(
                            type=openapi.TYPE_OBJECT, 
                            properties={
                                'room_id': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                                'room_name':openapi.Schema(type=openapi.TYPE_STRING, example="deluxe room"),
                                'default_rate': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, example=120.5)
                            }
                        ),
                        'overridden_rate':openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, example=120.5),
                        'stay_date': openapi.Schema(type=openapi.FORMAT_DATE, format=openapi.FORMAT_DATE, example='2024-07-10')
                    },
                ),
            ),
            400: "Invalid input",
            404: "Room/ Overridden room rate not found",
            500: "Internal server error",
        }
    )
    def put(self, request, room_id=None):
        if room_id is None:
            return Response({"error_message":"Room Id not provided"}, status=status.HTTP_400_BAD_REQUEST)

        stay_date=request.query_params.get('stay_date', None)
        if stay_date is None :
            return Response({"error_message":"Stay date not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            stay_date = datetime.strptime(stay_date, '%Y-%m-%d')
        except ValueError:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            room_rate = RoomRate.objects.get(room_id = room_id)
        except RoomRate.DoesNotExist:
            return Response({"error_message":"Room rate not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            overridden_room_rate = OverriddenRoomRate.objects.get(room_rate=room_rate,stay_date=stay_date)
        except OverriddenRoomRate.DoesNotExist:
            return Response({"error_message":"Overridden room rate not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = OverriddenRoomRateSerializer(overridden_room_rate, data=request.data, partial= True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Delete an existing overridden room rate by room id and stay date",
        manual_parameters=[
            openapi.Parameter(
                name="stay_date",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Stay date",
                required=True,
                example="2024-07-10",
            )
        ],
        responses={
            204: "Successful deletion",
            400: "Invalid input",
            404: "Room/ Overridden room rate not found",
            500: "Internal server error",
        }
    )
    def delete(self, request, room_id=None):
        if room_id is None:
            return Response({"error_message:Room Id is not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        stay_date=request.query_params.get('stay_date', None)
        if stay_date is None :
            return Response({"error_message":"Stay date not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            stay_date = datetime.strptime(stay_date, '%Y-%m-%d')
        except ValueError:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            room_rate = RoomRate.objects.get(room_id = room_id)
        except RoomRate.DoesNotExist:
            return Response({"error_message":"Room rate not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            overridden_room_rate = OverriddenRoomRate.objects.get(room_rate=room_rate,stay_date=stay_date)
        except OverriddenRoomRate.DoesNotExist:
            return Response({"error_message":"Overridden room rate not found"}, status=status.HTTP_404_NOT_FOUND)
        
        overridden_room_rate.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

        