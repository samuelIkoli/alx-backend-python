import mysql.connector
from mysql.connector import Error


def stream_user_ages():
    """
    Generator that streams user ages one by one from user_data table.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_password',   # <-- replace with your MySQL password
            database='ALX_prodev'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT age FROM user_data")

            # Single loop to yield each user's age
            for (age,) in cursor:
                yield float(age)

    except Error as e:
        print("Error streaming user ages:", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def calculate_average_age():
    """
    Consumes the generator to calculate the average age
    without loading all data into memory.
    """
    total = 0
    count = 0

    # Second (and last) loop
    for age in stream_user_ages():
        total += age
        count += 1

    avg_age = total / count if count > 0 else 0
    print(f"Average age of users: {avg_age:.2f}")


# Run script
if __name__ == "__main__":
    calculate_average_age()
