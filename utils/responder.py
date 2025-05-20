from rest_framework.response import Response
from .constants import Constant


class ResponseBuilder:

    @staticmethod
    def _build(code, http_status, data=None, errors=None):
        message = Constant.response_messages.get(code, "Unknown response code.")
        is_success = 200 <= http_status < 300

        response = {
            "status": is_success,
            "status_code": code,
            "message": message,
        }

        if is_success and data is not None:
            response["data"] = data
        elif not is_success and errors is not None:
            response["errors"] = errors

        return Response(response, status=http_status)

    @staticmethod
    def ok(code, data=None):
        return ResponseBuilder._build(code=code, http_status=200, data=data)

    @staticmethod
    def accepted(code, data=None):
        return ResponseBuilder._build(code=code, http_status=202, data=data)

    @staticmethod
    def bad_request(code, errors=None):
        return ResponseBuilder._build(code=code, http_status=400, errors=errors)

    @staticmethod
    def not_found(code, errors=None):
        return ResponseBuilder._build(code=code, http_status=404, errors=errors)
