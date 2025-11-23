import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename='requests.log',  # Log file path
    level=logging.INFO,
    format='%(message)s'
)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the user; if anonymous, set to "Anonymous"
        user = request.user if request.user.is_authenticated else "Anonymous"

        # Log the request
        logging.info(f"{datetime.now()} - User: {user} - Path: {request.path}")

        # Continue processing the request
        response = self.get_response(request)
        return response
