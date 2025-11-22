import sqlite3
import functools


# --------------------------
# Reuse decorator from task 1
# --------------------------
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper


# --------------------------
# Transaction management decorator
# --------------------------
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()       # commit if successful
            return result
        except Exception as e:
            conn.rollback()     # rollback on error
            raise e
    return wrapper


# --------------------------
# Update function using both decorators
# --------------------------
@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))


# Run update
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
