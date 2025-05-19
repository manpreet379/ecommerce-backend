# utils/response.py
from rest_framework.response import Response

def standard_response(data=None, message="", status="success", errors=None, status_code=200):
    response_body = {
        "status": status,
        "message": message,
        "data": data,
    }
    if errors:
        response_body["errors"] = errors
        
    return Response(response_body, status=status_code)
