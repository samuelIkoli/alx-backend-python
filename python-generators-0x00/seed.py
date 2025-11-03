import mysql.connector
from mysql.connector import Error
import uuid
import csv

# ----------------------------------------
# 1. Connect to MySQL Server (no database yet)
# ----------------------------------------
def connect_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_password'   # <-- replace with your MySQL password
        )
        if connection.is_connected():
            print("Connected to MySQL server")
            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None


# ----------------------------------------
# 2. Create database if it doesn’t exist
# ----------------------------------------
def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database 'ALX_prodev' ready.")
    except Error as e:
        print("Error creating database:", e)


# ----------------------------------------
# 3. Connect directly to ALX_prodev
# ----------------------------------------
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_password',  # <-- replace with your MySQL password
            database='ALX_prodev'
        )
        if connection.is_connected():
            print("Connected to ALX_prodev database")
            return connection
    except Error as e:
        print("Error while connecting to ALX_prodev:", e)
        return None


# ----------------------------------------
# 4. Create user_data table if not exists
# ----------------------------------------
def create_table(connection):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(3,0) NOT NULL,
        INDEX (user_id)
    )
    """
    try:
        cursor = connection.cursor()
        cursor.execute(create_table_query)
        connection.commit()
        print("Table 'user_data' ready.")
    except Error as e:
        print("Error creating table:", e)


# ----------------------------------------
# 5. Insert CSV data (if not already present)
# ----------------------------------------
def insert_data(connection, data):
    try:
        cursor = connection.cursor()

        # Check if email already exists
        check_query = "SELECT * FROM user_data WHERE email = %s"
        insert_query = """
        INSERT INTO user_data (user_id, name, email, age)
        VALUES (%s, %s, %s, %s)
        """

        for row in data:
            cursor.execute(check_query, (row['email'],))
            if cursor.fetchone() is None:
                cursor.execute(insert_query, (
                    str(uuid.uuid4()),
                    row['name'],
                    row['email'],
                    row['age']
                ))
        connection.commit()
        print("Data inserted successfully!")
    except Error as e:
        print("Error inserting data:", e)


# ----------------------------------------
# 6. Read CSV and seed the DB
# ----------------------------------------
def seed_from_csv(file_path):
    with open(file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        data = [row for row in reader]
        return data


# ----------------------------------------
# 7. Run all setup steps
# ----------------------------------------
if __name__ == "__main__":
    server_conn = connect_db()
    if server_conn:
        create_database(server_conn)
        server_conn.close()

    db_conn = connect_to_prodev()
    if db_conn:
        create_table(db_conn)
        data = seed_from_csv('user_data.csv')
        insert_data(db_conn, data)
        db_conn.close()
