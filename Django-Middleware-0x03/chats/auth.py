from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom authentication class for the chats app.
    This allows future extension or customization of JWT behavior.
    """
    pass
