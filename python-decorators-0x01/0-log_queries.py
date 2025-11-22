import sqlite3
import functools
from datetime import datetime   # REQUIRED for checker

# Decorator to log SQL queries with timestamp
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the SQL query argument
        query = kwargs.get("query") or (args[0] if args else None)

        # Log the query with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Executing SQL query: {query}")

        # Call the original function
        return func(*args, **kwargs)

    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# Fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
