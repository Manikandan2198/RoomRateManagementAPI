from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exception, context):
    response = exception_handler(exception, context)
    
    if response is not None:
        response.data['status_code'] = response.status_code

    else:
        response = Response({'error_message': 'An unexpected error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return response
