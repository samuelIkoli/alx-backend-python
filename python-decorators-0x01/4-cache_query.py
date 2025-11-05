from functools import wraps
import hashlib
import pickle
import time

# In-memory cache store
_cache_store = {}

def cache_db_results(ttl=60):
    """
    Decorator that caches results of database queries
    to avoid redundant DB calls.

    - ttl: time-to-live in seconds (default: 60s)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create a unique cache key based on function name + args
            key_data = (func.__name__, args, tuple(sorted(kwargs.items())))
            cache_key = hashlib.sha256(pickle.dumps(key_data)).hexdigest()

            # Check if result is cached and still valid
            if cache_key in _cache_store:
                result, timestamp = _cache_store[cache_key]
                if time.time() - timestamp < ttl:
                    print(f"⚡ Cache hit for '{func.__name__}'")
                    return result
                else:
                    # Cache expired
                    del _cache_store[cache_key]

            # Otherwise, execute the function and cache its result
            print(f"🗄️ Cache miss for '{func.__name__}' — querying database...")
            result = func(*args, **kwargs)
            _cache_store[cache_key] = (result, time.time())
            return result
        return wrapper
    return decorator
