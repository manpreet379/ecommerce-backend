from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework import status
import logging

from .responder import standard_response

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    response = drf_exception_handler(exc, context)

    view_name = context.get('view', context).__class__.__name__

    if response is not None:
        detail = response.data.get("detail", str(response.data))
        logger.warning(f"[Handled] {view_name}: {detail}")
        return standard_response(
            data=None,
            message=detail,
            status="error",
            errors=response.data,
            status_code=response.status_code
        )

    # Unhandled exceptions
    logger.error(f"[Unhandled] {view_name}: {str(exc)}", exc_info=True)
    return standard_response(
        data=None,
        message="Internal server error",
        status="error",
        errors=str(exc),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
