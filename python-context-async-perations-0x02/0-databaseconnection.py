import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    """
    Custom context manager that handles opening and closing
    a MySQL database connection automatically.
    """
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def __enter__(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor(dictionary=True)
            print("✅ Database connection opened.")
            return self.cursor
        except Error as e:
            print("❌ Error while connecting to database:", e)
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("🔒 Database connection closed.")
        # Return False to re-raise any exception that occurs inside the with block
        return False

with DatabaseConnection(...) as cursor:
    cursor.execute("SELECT * FROM users")
    print(cursor.fetchall())