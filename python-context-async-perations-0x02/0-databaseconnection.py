import sqlite3


class DatabaseConnection:
    """Custom context manager to handle SQLite DB connections."""

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        # Open database connection
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        # Close the connection whether or not an exception occurred
        if self.conn:
            self.conn.close()

        # Returning False means exceptions (if any) are NOT suppressed
        return False


# Using the context manager to fetch users
with DatabaseConnection("users.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print(results)
