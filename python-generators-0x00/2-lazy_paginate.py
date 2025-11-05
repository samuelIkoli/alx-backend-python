import mysql.connector
from mysql.connector import Error

def paginate_users(page_size, offset):
    """
    Fetches a single page of users from user_data table starting at a given offset.
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
            query = f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}"
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows

    except Error as e:
        print("Error fetching page:", e)
        return []

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def lazy_paginate(page_size):
    """
    Generator that lazily fetches pages of users one by one.
    Only loads the next page when needed (lazy loading).
    Must use only one loop.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size  # move to the next page


# Example usage:
if __name__ == "__main__":
    for page in lazy_paginate(3):
        print("New Page:")
        for user in page:
            print(user)
