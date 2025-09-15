from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError


def custom_exception_handler(exc, context):
    response = drf_exception_handler(exc, context)
    if response is None:
        if isinstance(exc, IntegrityError):
            return Response(
                {"detail": "Integrity error"}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {"detail": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return response
