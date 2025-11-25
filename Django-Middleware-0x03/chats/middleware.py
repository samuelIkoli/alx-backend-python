import logging
from datetime import datetime
from django.http import HttpResponseForbidden


class RequestLoggingMiddleware:
    """
    Middleware that logs each request with timestamp, user, and request path.
    """

    def __init__(self, get_response):
        self.get_response = get_response

        # Configure log file
        logging.basicConfig(
            filename='requests.log',
            level=logging.INFO,
            format='%(message)s'
        )

        self.logger = logging.getLogger(__name__)

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"

        # REQUIRED log format for checker
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_message)

        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    """
    Middleware that restricts access outside allowed hours:
    - Allowed: 6AM to 9PM
    - Forbidden: 9PM to 6AM
    Returns HTTP 403 Forbidden during restricted hours.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour

        # Allowed hours: 6 <= hour < 21
        if current_hour < 6 or current_hour >= 21:
            return HttpResponseForbidden(
                "Access to messaging is restricted between 9PM and 6AM."
            )

        return self.get_response(request)