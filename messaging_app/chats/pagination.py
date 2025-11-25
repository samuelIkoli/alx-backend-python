from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    """
    Custom pagination for messages.
    Returns 20 messages per page by default.
    """
    page_size = 20
    page_size_query_param = 'page_size'   # optional override
    max_page_size = 100