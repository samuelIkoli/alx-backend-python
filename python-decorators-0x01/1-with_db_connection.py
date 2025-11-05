import mysql.connector
from mysql.connector import Error
from functools import wraps

def with_db_connection(func):
    """
    Decorator that automatically handles opening and closing
    a MySQL database connection for the wrapped function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        connection = None
        try:
            # Open connection
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='your_password',  # <-- replace with your DB password
                database='ALX_prodev'
            )

            if connection.is_connected():
                print(f"✅ Database connected for '{func.__name__}'")

                # Pass the connection as a keyword argument
                result = func(*args, connection=connection, **kwargs)
                return result

        except Error as e:
            print(f"❌ Database error in '{func.__name__}':", e)

        finally:
            # Close the connection automatically
            if connection and connection.is_connected():
                connection.close()
                print(f"🔒 Database connection closed after '{func.__name__}'")

    return wrapper
