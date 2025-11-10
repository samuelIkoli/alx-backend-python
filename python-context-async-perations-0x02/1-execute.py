import mysql.connector
from mysql.connector import Error

class ExecuteQuery:
    """
    A reusable context manager that connects to the database,
    executes a given SQL query with parameters, and returns the results.
    """
    def __init__(self, query, params=None):
        self.query = query
        self.params = params
        self.connection = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        try:
            # Establish DB connection
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='your_password',  # <-- replace with your MySQL password
                database='ALX_prodev'
            )
            self.cursor = self.connection.cursor(dictionary=True)

            print("✅ Connected to database.")

            # Execute the provided query with parameters
            if self.params:
                self.cursor.execute(self.query, self.params)
            else:
                self.cursor.execute(self.query)

            # Fetch results
            self.results = self.cursor.fetchall()
            return self.results

        except Error as e:
            print("❌ Error while executing query:", e)
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Always clean up
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("🔒 Database connection closed.")
        # Returning False means exceptions (if any) are not suppressed
        return False
