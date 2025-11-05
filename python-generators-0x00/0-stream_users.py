import mysql.connector
from mysql.connector import Error

def stream_users():
    """
    Generator function that fetches rows one by one
    from the user_data table using yield.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='alx',
            password='password',
            database='ALX_prodev'
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data")

            # single loop — yields each row as it's fetched
            for row in cursor:
                yield row

    except Error as e:
        print("Error while streaming data:", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# Example usage (optional):
if __name__ == "__main__":
    for user in stream_users():
        print(user)
