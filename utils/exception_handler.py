from rest_framework.views import exception_handler as drf_exception_handler
import logging
from .responder import ResponseBuilder 
from .constants import Constant

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    print("custom_exception_handler called")
    response = drf_exception_handler(exc, context)

    view_name = context.get('view', context).__class__.__name__

    if response is not None:
        detail = response.data.get("detail", str(response.data))
        logger.warning(f"[Handled] {view_name}: {detail}")

        http_code = response.status_code

        code_map = {
            400: 507,
            401: 504,
            403: 506,
            404: 501,
            405: 505,
            500: 500,
        }
        mapped_code = code_map.get(http_code, 500)
       
        return ResponseBuilder.bad_request(code=mapped_code, errors=response.data, )

    logger.error(f"[Unhandled] {view_name}: {str(exc)}", exc_info=True)
    return ResponseBuilder.bad_request(
        code=500,
        errors=str(exc)
    )
