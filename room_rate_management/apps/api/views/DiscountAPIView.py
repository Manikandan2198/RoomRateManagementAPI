from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.models import Discount
from apps.api.serializers import DiscountSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Create your views here.

class DiscountListAPI(APIView):
    @swagger_auto_schema(
        operation_description="Get all discounts",
        responses={
            200: openapi.Response(
                description="Successful operation",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'discount_id': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                            'dicount_name':openapi.Schema(type=openapi.TYPE_STRING, example="summer discount"),
                            'discount_type':openapi.Schema(type=openapi.TYPE_STRING, example="fixed, percentage"),
                            'discount_value': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, example=20)
                        },
                    ),
                ),
            ),
            500: "Internal server error",
        }
    )
    def get(self, request): 
        discounts = Discount.objects.all()
        serializer = DiscountSerializer(discounts, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Create a new discount",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'discount_name':openapi.Schema(type=openapi.TYPE_STRING, example="summer discount"),
                'discount_type':openapi.Schema(type=openapi.TYPE_STRING, example="fixed, percentage"),
                'discount_value': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, example=20)
            },
        ),
        responses={
            201: openapi.Response(
                description="Successful operation",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'discount_id': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                        'dicount_name':openapi.Schema(type=openapi.TYPE_STRING, example="summer discount"),
                        'discount_type':openapi.Schema(type=openapi.TYPE_STRING, example="fixed, percentage"),
                        'discount_value': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, example=20)
                    },
                ),
            ),
            400: "Invalid input",
            500: "Internal server error",
        }
    )
    def post(self, request):
        serializer = DiscountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DiscountDetailAPI(APIView):
    @swagger_auto_schema(
        operation_description="Get discount for a specific discount id",
        responses={
            200: openapi.Response(
                description="Successful operation",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'discount_id': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                        'dicount_name':openapi.Schema(type=openapi.TYPE_STRING, example="summer discount"),
                        'discount_type':openapi.Schema(type=openapi.TYPE_STRING, example="fixed, percentage"),
                        'discount_value': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, example=20)
                    }
                ),
            ),
            400: "invalid input",
            404: "Discount not found",
            500: "Internal server error",
        }
    )
    def get(self, request,discount_id=None): 
        if discount_id is None:
            return Response({"error_message: Discount id is not provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            discount = Discount.objects.get(discount_id = discount_id)
        except Discount.DoesNotExist:
            return Response({"error_message":"Discount not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = DiscountSerializer(discount)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Update an existing discount",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'dicount_name':openapi.Schema(type=openapi.TYPE_STRING, example="summer discount"),
                'discount_type':openapi.Schema(type=openapi.TYPE_STRING, example="fixed, percentage"),
                'discount_value': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, example=20)
            },
        ),
        responses={
            201: openapi.Response(
                description="Successful operation",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'discount_id': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                        'dicount_name':openapi.Schema(type=openapi.TYPE_STRING, example="summer discount"),
                        'discount_type':openapi.Schema(type=openapi.TYPE_STRING, example="fixed, percentage"),
                        'discount_value': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, example=20)
                    },
                ),
            ),
            400: "Invalid input",
            404: "Discount not found",
            500: "Internal server error",
        }
    )
    def put(self, request, discount_id=None):
        if discount_id is None:
            return Response({"error_message":"discount id not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            discount = Discount.objects.get(discount_id=discount_id)
        except Discount.DoesNotExist:
            return Response({"error_message":"Discount not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = DiscountSerializer(discount, data=request.data, partial= True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Delete an existing discount",
        responses={
            204: "Successful deletion",
            400: "Invalid input",
            404: "Room rate not found",
            500: "Internal server error"
        }
    )
    def delete(self, request, discount_id=None):
        if discount_id is None:
            return Response({"error_message: Discount id is not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            discount = Discount.objects.get(discount_id=discount_id)
        except Discount.DoesNotExist:
            return Response({"error_message":"Discount not found"}, status=status.HTTP_404_NOT_FOUND)
        discount.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

        