from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.models import RoomRate
from apps.api.serializers import RoomRateSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Create your views here.

class RoomRateListAPI(APIView):

    @swagger_auto_schema(
        operation_description="Get all room rates",
        responses={
            200: openapi.Response(
                description="Successful operation",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'room_id': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                            'room_name':openapi.Schema(type=openapi.TYPE_STRING, example="deluxe room"),
                            'default_rate': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, example=120.5)
                        },
                    ),
                ),
            ),
            500: "Internal server error",
        }
    )
    def get(self, request): 
        room_rates = RoomRate.objects.all()
        serializer = RoomRateSerializer(room_rates, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Create a new room rate",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'room_name':openapi.Schema(type=openapi.TYPE_STRING, example="deluxe room"),
                'default_rate': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, example=120.5)
            },
        ),
        responses={
            201: openapi.Response(
                description="Successful operation",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'room_id': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                        'room_name':openapi.Schema(type=openapi.TYPE_STRING, example="deluxe room"),
                        'default_rate': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, example=120.5)
                    },
                ),
            ),
            400: "Invalid input",
            500: "Internal server error",
        }
    )
    def post(self, request):
        serializer = RoomRateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RoomRateDetailAPI(APIView):
    @swagger_auto_schema(
        operation_description="Get room rate for a specific room id",
        responses={
            200: openapi.Response(
                description="Successful operation",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'room_id': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                        'room_name':openapi.Schema(type=openapi.TYPE_STRING, example="deluxe room"),
                        'default_rate': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, example=120.5)
                    }
                ),
            ),
            400: "invalid input",
            404: "Room rate not found",
            500: "Internal server error",
        }
    )
    def get(self, request,room_id=None): 
        if room_id is None:
            return Response({"error_message":"Room rate id not provided"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            room_rate = RoomRate.objects.get(room_id = room_id)
        except RoomRate.DoesNotExist:
            return Response({"error_message":"Room rate not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = RoomRateSerializer(room_rate)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    
    @swagger_auto_schema(
        operation_description="Update an existing room rate",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'room_name':openapi.Schema(type=openapi.TYPE_STRING, example="deluxe room"),
                'default_rate': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, example=120.5)
            },
        ),
        responses={
            201: openapi.Response(
                description="Successful operation",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'room_name':openapi.Schema(type=openapi.TYPE_STRING, example="deluxe room"),
                        'default_rate': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, example=120.5)
                    },
                ),
            ),
            400: "Invalid input",
            404: "Room not found",
            500: "Internal server error",
        }
    )
    def put(self, request, room_id=None):
        if room_id is None:
            return Response({"error_message":"Room id not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            room_rate = RoomRate.objects.get(room_id=room_id)
        except RoomRate.DoesNotExist:
            return Response({"error_message":"Room not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = RoomRateSerializer(room_rate, data=request.data, partial= True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Delete an existing room rate",
        responses={
            204: "Successful deletion",
            400: "Invalid input",
            404: "Room rate not found",
            500: "Internal server error"
        }
    )
    def delete(self, request, room_id=None):
        if room_id is None:
            return Response({"error_message: Room id is not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            room_rate = RoomRate.objects.get(room_id=room_id)
        except RoomRate.DoesNotExist:
            return Response({"error_message":"Room not found"}, status=status.HTTP_404_NOT_FOUND)
        room_rate.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

        