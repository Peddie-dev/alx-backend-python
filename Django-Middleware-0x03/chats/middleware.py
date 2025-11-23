from datetime import datetime
from django.http import HttpResponseForbidden


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Current server time
        now = datetime.now().time()

        # Define allowed access window (6 PM to 9 PM)
        start_time = datetime.strptime("18:00", "%H:%M").time()
        end_time = datetime.strptime("21:00", "%H:%M").time()

        # If current time is outside the allowed range, deny access
        if not (start_time <= now <= end_time):
            return HttpResponseForbidden("Access to messaging is only allowed between 6PM and 9PM.")

        # Proceed normally if within allowed time
        response = self.get_response(request)
        return response
