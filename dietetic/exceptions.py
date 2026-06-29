# dietetic/exceptions.py
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    # Llama al manejador por defecto de DRF para obtener la respuesta estándar
    response = exception_handler(exc, context)


    if response is not None:
        response.data['status_code'] = response.status_code
        response.data['success'] = False
        return response

    logger.exception("Error no controlado detectado: %s", str(exc))

    return Response(
        {
            'success': False,
            'status_code': 500,
            'detail': 'Ha ocurrido un error interno en el servidor.',
            'error': str(exc)
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
