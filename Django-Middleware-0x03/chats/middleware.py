import logging
from datetime import datetime, timedelta
from django.http import HttpResponseForbidden, HttpResponse


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
    

class OffensiveLanguageMiddleware:
    """
    Middleware that limits number of POST chat messages
    from the same IP address to 5 per minute.
    """

    def __init__(self, get_response):
        self.get_response = get_response

        # Store: { ip_address: [timestamps] }
        self.message_history = {}

    def __call__(self, request):
        ip = request.META.get("REMOTE_ADDR")

        # We only rate-limit POST requests (sending messages)
        if request.method == "POST" and "/messages/" in request.path:
            now = datetime.now()

            # Initialize message history for new IPs
            if ip not in self.message_history:
                self.message_history[ip] = []

            # Remove timestamps older than 1 minute
            one_minute_ago = now - timedelta(minutes=1)
            self.message_history[ip] = [
                ts for ts in self.message_history[ip] if ts > one_minute_ago
            ]

            # Check if limit exceeded
            if len(self.message_history[ip]) >= 5:
                return HttpResponse(
                    "Rate limit exceeded: You can only send 5 messages per minute.",
                    status=429
                )

            # Add current request timestamp
            self.message_history[ip].append(now)

        return self.get_response(request)
    
class RolepermissionMiddleware:
    """
    Middleware that allows only admins or moderators
    to access protected endpoints.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        # Only check role if user is authenticated
        if user.is_authenticated:

            # If your User model uses `role` field: guest/host/admin/moderator
            user_role = getattr(user, "role", None)

            # Block if user is not admin or moderator
            if user_role not in ["admin", "moderator"]:
                return HttpResponseForbidden(
                    "Access denied: You do not have permission to perform this action."
                )

        return self.get_response(request)