from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR

def custom_exception_handler(exc, context) -> Response:
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response: Response|None = exception_handler(exc, context)
    custom_response_data = dict()

    if response and response.data and 'detail' in response.data:
        custom_response_data['error_code'] = exc.get_codes()
        custom_response_data['error_message'] = response.data['detail']
        return Response(custom_response_data, status=exc.status_code)

    # Shouldn't reach here, but if it does, return a generic error message
    custom_response_data['error_code'] = "000"
    custom_response_data['error_message'] = "Unknown error occurred"
    return Response(custom_response_data, status=HTTP_500_INTERNAL_SERVER_ERROR)

