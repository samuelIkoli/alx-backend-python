import logging
from datetime import datetime

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
