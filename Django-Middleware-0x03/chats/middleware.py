import logging
from datetime import datetime
from django.http import HttpResponseForbidden, JsonResponse
import time

# ----------------------------
# Configure logging
# ----------------------------
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


# ----------------------------
# Middleware 3: Rate Limiting per IP
# ----------------------------
class OffensiveLanguageMiddleware:
    """
    Middleware to limit number of messages per IP address.
    Each IP can send up to 5 messages per minute.
    """
    ip_requests = {}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only track POST requests to chat
        if request.method == "POST" and request.path.startswith("/chats/"):
            ip = self.get_client_ip(request)
            now = time.time()

            # Initialize list for IP if not exists
            if ip not in self.ip_requests:
                self.ip_requests[ip] = []

            # Remove timestamps older than 60 seconds
            self.ip_requests[ip] = [ts for ts in self.ip_requests[ip] if now - ts < 60]

            # Check rate limit
            if len(self.ip_requests[ip]) >= 5:
                logging.info(f"{datetime.now()} - IP: {ip} - Path: {request.path} - BLOCKED [RATE LIMIT]")
                return JsonResponse(
                    {"error": "Rate limit exceeded. Maximum 5 messages per minute."},
                    status=429
                )

            # Record current timestamp
            self.ip_requests[ip].append(now)

        response = self.get_response(request)
        return response

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

