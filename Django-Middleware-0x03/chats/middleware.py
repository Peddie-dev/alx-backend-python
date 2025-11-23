import logging
from datetime import datetime
from django.http import HttpResponseForbidden

# Configure logging
logging.basicConfig(
    filename='requests.log',
    level=logging.INFO,
    format='%(message)s'
)

# ----------------------------
# Middleware 1: Request Logging
# ----------------------------
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        logging.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        response = self.get_response(request)
        return response


# ----------------------------
# Middleware 2: Restrict Access by Time
# ----------------------------
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()
        start_time = datetime.strptime("18:00", "%H:%M").time()
        end_time = datetime.strptime("21:00", "%H:%M").time()

        if not (start_time <= now <= end_time):
            return HttpResponseForbidden(
                "Access to messaging is only allowed between 6PM and 9PM."
            )

        response = self.get_response(request)
        return response

