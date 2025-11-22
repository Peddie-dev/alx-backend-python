import time
import sqlite3
import functools


# ---------------------------------------------
# Reuse with_db_connection decorator from Task 1
# ---------------------------------------------
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper


# ---------------------------------------------
# Retry decorator for transient DB failures
# ---------------------------------------------
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0

            while attempt < retries:
                try:
                    return func(*args, **kwargs)

                except Exception as e:
                    attempt += 1
                    print(f"Attempt {attempt} failed: {e}")

                    # If out of retries → raise the error
                    if attempt == retries:
                        raise

                    # Wait before retrying
                    time.sleep(delay)

        return wrapper
    return decorator


# ---------------------------------------------
# Function wrapped with both decorators
# ---------------------------------------------
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


# ---------------------------------------------
# Attempt to fetch users with auto retry
# ---------------------------------------------
users = fetch_users_with_retry()
print(users)
