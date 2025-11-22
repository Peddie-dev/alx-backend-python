import time
import sqlite3
import functools


# Global cache dictionary
query_cache = {}


# -------------------------------------------------
# with_db_connection (copied from previous tasks)
# -------------------------------------------------
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper


# -------------------------------------------------
# Cache decorator
# -------------------------------------------------
def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract SQL query from kwargs or args
        query = kwargs.get("query")

        # If query not in kwargs, assume it's the second argument
        if query is None and len(args) > 1:
            query = args[1]

        # Check cache
        if query in query_cache:
            print("Returning cached result...")
            return query_cache[query]

        # Execute the function and store its result
        result = func(*args, **kwargs)
        query_cache[query] = result
        print("Query cached!")
        return result

    return wrapper


# -------------------------------------------------
# Function using both decorators
# -------------------------------------------------
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# -------------------------------------------------
# Calls
# -------------------------------------------------

# First call → hits database and caches result
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call → returns cached response
users_again = fetch_users_with_cache(query="SELECT * FROM users")
