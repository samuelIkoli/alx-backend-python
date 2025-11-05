import mysql.connector
from mysql.connector import Error

def stream_users_in_batches(batch_size):
    """
    Generator that fetches rows from user_data table in batches.
    Uses yield to return each batch as a list of user dicts.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='alx',
            password='password',   # <-- replace with your MySQL password
            database='ALX_prodev'
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data")

            while True:
                batch = cursor.fetchmany(batch_size)
                if not batch:
                    break
                yield batch  # yield one batch at a time

    except Error as e:
        print("Error while fetching data in batches:", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def batch_processing(batch_size):
    """
    Processes each batch yielded from stream_users_in_batches()
    and filters users over age 25.
    """
    for batch in stream_users_in_batches(batch_size):     # Loop 1
        filtered_users = [user for user in batch if int(user['age']) > 25]  # Loop 2 (list comprehension)
        for user in filtered_users:  # Loop 3
            yield user


# Example usage:
if __name__ == "__main__":
    print("Users over age 25:")
    for user in batch_processing(5):
        print(user)
