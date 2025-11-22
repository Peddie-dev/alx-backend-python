import sqlite3

class ExecuteQuery:
    """Reusable context manager that executes a query and returns the results."""

    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params if params else ()
        self.conn = None
        self.results = None

    def __enter__(self):
        # Open the connection
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()

        # Execute the query with parameters
        cursor.execute(self.query, self.params)
        self.results = cursor.fetchall()

        return self.results   # What the with-statement receives

    def __exit__(self, exc_type, exc_value, traceback):
        # Close the connection safely
        if self.conn:
            self.conn.close()

        # Do not suppress exceptions
        return False


# Example usage:
query = "SELECT * FROM users WHERE age > ?"
param_value = 25

with ExecuteQuery("users.db", query, (param_value,)) as results:
    print(results)
