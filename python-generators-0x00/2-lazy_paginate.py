#!/usr/bin/python3
"""
2-lazy_paginate.py - Lazily paginate user_data from ALX_prodev
"""

seed = __import__('seed')


def paginate_users(page_size, offset):
    """
    Fetch a single page of rows from user_data
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator that lazily fetches pages of user_data.
    Each page contains `page_size` rows.
    """
    offset = 0

    while True:  # Only one loop
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
