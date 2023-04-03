from rest_framework.response import Response

class ExpiresResponse(Response):
    headers={"Access-Control-Max-Age":"2592000"}