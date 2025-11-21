#!/usr/bin/python3
"""
1-batch_processing.py - batch processing generator for user_data
"""

import mysql.connector
from mysql.connector import Error
seed = __import__('seed')


def stream_users_in_batches(batch_size):
    """
    Generator that fetches rows from user_data in batches.
    Each batch is a list of dictionaries.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Bondeni001.",  # update with your MySQL password
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        while True:  # Single loop
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch  # yield the batch instead of returning

        cursor.close()
        connection.close()

    except Error as e:
        print(f"Error: {e}")


def batch_processing(batch_size):
    """
    Processes each batch from stream_users_in_batches and
    yields users over 25 years old.
    """
    for batch in stream_users_in_batches(batch_size):  # Loop 1: batches
        for user in batch:  # Loop 2: users in batch
            if user["age"] > 25:  # Filter condition
                yield user  # <-- use yield instead of print

