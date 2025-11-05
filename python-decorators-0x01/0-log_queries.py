from functools import wraps
from django.db import connection

def log_db_queries(func):
    """
    Decorator that logs all SQL queries executed by a function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Clear previous queries
        connection.queries_log.clear() if hasattr(connection, 'queries_log') else None

        # Record initial query count
        before = len(connection.queries)

        result = func(*args, **kwargs)

        # Capture new queries executed by the function
        after = len(connection.queries)
        executed = connection.queries[before:after]

        if executed:
            print(f"\n📘 Database queries executed by '{func.__name__}':")
            for i, query in enumerate(executed, start=1):
                print(f"  {i}. {query['sql']} (Time: {query['time']}s)")
        else:
            print(f"\n✅ '{func.__name__}' executed with no database queries.")

        return result

    return wrapper
