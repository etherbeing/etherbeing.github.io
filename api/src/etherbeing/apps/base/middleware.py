from django.conf import settings
from django.http import HttpResponse


class LocalCorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        origin = request.headers.get("Origin")
        if request.method == "OPTIONS":
            response = HttpResponse(status=200)
        else:
            response = self.get_response(request)

        if origin and origin in getattr(settings, "CORS_ALLOWED_ORIGINS", []):
            response["Access-Control-Allow-Origin"] = origin
            response["Vary"] = "Origin"
            response["Access-Control-Allow-Credentials"] = "true"
            response["Access-Control-Allow-Headers"] = (
                "Accept, Authorization, Content-Type, Origin, User-Agent, X-CSRFToken, X-Requested-With"
            )
            response["Access-Control-Allow-Methods"] = (
                "DELETE, GET, OPTIONS, PATCH, POST, PUT"
            )

        return response
