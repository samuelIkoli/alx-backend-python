import mysql.connector
from mysql.connector import Error
from functools import wraps
import time

def log_db_queries(func):
    """
    Decorator that logs SQL queries executed by a function
    using mysql.connector instead of Django ORM.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        connection = None
        cursor = None

        try:
            # Connect to MySQL
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='your_password',  # <-- replace with your password
                database='ALX_prodev'
            )
            cursor = connection.cursor()

            print(f"🔗 Connected to MySQL for '{func.__name__}'")

            # Start timing
            start_time = time.time()

            # Pass the cursor or connection to the wrapped function
            result = func(*args, connection=connection, cursor=cursor, **kwargs)

            # End timing
            elapsed = time.time() - start_time
            print(f"✅ '{func.__name__}' executed successfully in {elapsed:.4f}s")

            return result

        except Error as e:
            print(f"❌ Database error in '{func.__name__}': {e}")

        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()
                print(f"🔒 MySQL connection closed for '{func.__name__}'")

    return wrapper
