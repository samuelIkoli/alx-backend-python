import mysql.connector
from mysql.connector import Error
from functools import wraps

def transactional(func):
    """
    Decorator that manages a database transaction automatically.
    It commits on success and rolls back on error.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        connection = None
        try:
            # Open database connection
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='your_password',  # <-- replace with your MySQL password
                database='ALX_prodev'
            )

            if connection.is_connected():
                cursor = connection.cursor(dictionary=True)
                print(f"✅ Transaction started for '{func.__name__}'")

                # Inject connection and cursor into function
                result = func(*args, connection=connection, cursor=cursor, **kwargs)

                # Commit changes if successful
                connection.commit()
                print(f"💾 Transaction committed for '{func.__name__}'")
                return result

        except Error as e:
            # Roll back if error occurs
            if connection:
                connection.rollback()
                print(f"⚠️ Transaction rolled back for '{func.__name__}' due to error: {e}")
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()
                print(f"🔒 Connection closed for '{func.__name__}'")

    return wrapper
