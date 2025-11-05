import time
import mysql.connector
from mysql.connector import Error, OperationalError, InterfaceError, DatabaseError
from functools import wraps

def retry_on_transient_errors(max_retries=3, delay=1, backoff=2):
    """
    Decorator that retries a database operation if it fails due to transient errors.
    - max_retries: number of times to retry
    - delay: initial delay (seconds)
    - backoff: multiplier for exponential backoff (delay *= backoff)
    """
    transient_errors = (
        OperationalError,
        InterfaceError,
        DatabaseError,
    )

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            current_delay = delay

            while retries < max_retries:
                try:
                    # Attempt database operation
                    return func(*args, **kwargs)

                except transient_errors as e:
                    retries += 1
                    print(f"⚠️ Transient DB error in '{func.__name__}': {e}")
                    if retries < max_retries:
                        print(f"🔁 Retrying ({retries}/{max_retries}) in {current_delay}s...")
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        print(f"❌ Max retries reached for '{func.__name__}'. Operation failed.")
                        raise
        return wrapper
    return decorator
